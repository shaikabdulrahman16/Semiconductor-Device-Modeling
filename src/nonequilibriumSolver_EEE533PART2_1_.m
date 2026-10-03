%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%               1D Drift–Diffusion PN Diode (Gummel + SG)                %%
%%                       (Silicon, T = 300 K, SRH)                         %%
%%                                                                         %%
%%  Uses absorbed equilibrium solver style, LU_Decomposition, and berfun.  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear; clc;

%% ----------------------- Physical / Material Consts -----------------------
q    = 1.602e-19;           % [C]
kb   = 1.380e-23;           % [J/K]
T    = 300;                 % [K]
Vt   = kb*T/q;              % [V] ~ 0.02585 at 300K
eps  = 1.05e-12;            % [F/cm]  (given as 1.05e-10 F/m)
ni   = 1.5e10;              % [cm^-3]  intrinsic conc.

% For band-edge plots (same convention as equilibrium solver you absorbed)
RNc = 2.8e19;            % [cm^-3]
Eg  = 1.12;              % [eV]
dEc = Vt*log(RNc/ni);    % [eV] conduction-band offset so that EF,eq = 0 reference

% Constant mobilities (given): [cm^2/V-s]
mu_n = 1650;
mu_p = 650;

% Einstein relation
Dn = mu_n*Vt;               % [cm^2/s]
Dp = mu_p*Vt;               % [cm^2/s]

% SRH lifetimes (given): traps at intrinsic level
TAUN0 = 10e-6;              % [s]
TAUP0 = 10e-6;              % [s]

%% ---------------------------- Device / Doping -----------------------------
Na = 1e17;                  % [cm^-3] p-side
Nd = 1e17;                  % [cm^-3] n-side

% Region extents
x_n = 0.5e-4;               % [cm] n-region length
x_p = 0.5e-4;               % [cm] p-region length
x_max = x_n + x_p;

% Debye lengths for grid sizing (extrinsic)
Ldn = sqrt(eps*Vt/(q*Nd));  % [cm]
Ldp = sqrt(eps*Vt/(q*Na));  % [cm]
Ldi = sqrt(eps*Vt/(q*ni));  % [cm]

% Pick smallest and refine
dx = min(Ldn, Ldp)/5;       % [cm]
N  = round(x_max/dx);       % number of nodes
dx = x_max/N;               % re-normalize for integer N
x  = (0:N-1)'*dx;           % [cm], left->right

% Doping profile (Nd - Na), normalized by ni (as in absorbed code style)
dop = zeros(N,1);
for i = 1:N
    if x(i) <= x_n
        dop(i) = Nd/ni;     % n-side
    else
        dop(i) = -Na/ni;    % p-side
    end
end

%% ------------------------------ Initialization ----------------------------
% Charge neutrality–based initial guess (absorbed style)
fi  = zeros(N,1);  % dimensionless potential phi = ln(n/ni)
n   = zeros(N,1);  % [cm^-3]
p   = zeros(N,1);  % [cm^-3]

for i = 1:N
    zz = 0.5*dop(i);
    if zz > 0
        xx = zz*(1 + sqrt(1+1/(zz*zz)));
    elseif zz < 0
        xx = zz*(1 - sqrt(1+1/(zz*zz)));
    else
        xx = 1; % intrinsic
    end
    fi(i) = log(xx);
    n(i)  = ni*exp(fi(i));
    p(i)  = ni*exp(-fi(i));
end

%% --------------------------- Bias Sweep Settings --------------------------
Vmax   = 0.8;                 % [V]
dV     = 0.5*Vt;              % stable increment: fraction of Vt
Vlist  = 0:dV:Vmax;
nBias  = numel(Vlist);

% Convergence params
tol_inner = 1e-10;            % Gummel inner loop tolerance on max relative update
tol_poi   = 1e-9;             % Poisson linearization tolerance (dimensionless fi)
max_iter  = 500;              % Gummel iterations per bias
max_poi   = 500;              % Poisson iterations per Gummel step

% Preallocate I–V
J_total = zeros(nBias,1);     % [A/cm^2]

% Snapshots to compare equilibrium vs. VA=0.75 V
fi_eq = []; n_eq = []; p_eq = [];
fi_075 = []; n_075 = []; p_075 = [];

%% ------------------------------- Main Sweep -------------------------------
for kv = 1:nBias
    VA = Vlist(kv);  % forward bias (Anode at p-side, Cathode at n-side)

    % Ohmic contacts: majority fixed, minority scale by exp(VA/Vt)
    % Left contact (n-side, x=0):
    nL = Nd;                         % majority electrons ~ Nd
    pL = (ni^2/Nd)*exp(VA/Vt);       % injected holes
    % Right contact (p-side, x=L):
    pR = Na;                         % majority holes ~ Na
    nR = (ni^2/Na)*exp(VA/Vt);       % injected electrons

    % Dirichlet for Poisson from boundary carrier densities:
    fiL = log(nL/ni);
    fiR = log(nR/ni);

    % Gummel iterations
    for it = 1:max_iter
        n_old = n; p_old = p; fi_old = fi;

        % -------------------------- (1) Solve Poisson --------------------------
        % Linearized Poisson with current n, p (absorbed style)
        dx2 = dx*dx;
        a = zeros(N,1); b = zeros(N,1); c = zeros(N,1); f = zeros(N,1);

        % internal nodes
        for i = 2:N-1
            a(i) =  1/dx2;
            c(i) =  1/dx2;
            % b(i) & f(i) from linearization around fi using n=ni*exp(fi), p=ni*exp(-fi)
            b(i) = -(2/dx2 + exp(fi(i)) + exp(-fi(i)));
            f(i) =  (exp(fi(i)) - exp(-fi(i)) - dop(i)) ...
                    - fi(i)*(exp(fi(i)) + exp(-fi(i)));
        end
        % Dirichlet BC
        b(1) = 1; f(1) = fiL;
        b(N) = 1; f(N) = fiR;

        % Newton–like linearization loop for Poisson
        for ip = 1:max_poi
            fi_new = LU_Decomposition(a,b,c,f,N);
            if max(abs(fi_new - fi)) < tol_poi
                fi = fi_new; break;
            end
            % Update coefficients around new fi
            fi = fi_new;
            for i = 2:N-1
                b(i) = -(2/dx2 + exp(fi(i)) + exp(-fi(i)));
                f(i) =  (exp(fi(i)) - exp(-fi(i)) - dop(i)) ...
                        - fi(i)*(exp(fi(i)) + exp(-fi(i)));
            end
            f(1)=fiL; f(N)=fiR;
        end

        % Update carrier densities to be consistent with fi (good Gummel seed)
        n = ni*exp(fi); p = ni*exp(-fi);

        % Enforce contact Dirichlet values for carriers (ohmic)
        n(1)=nL; p(1)=pL; n(N)=nR; p(N)=pR;

        % -------------------- (2) Solve electron continuity --------------------
        % SG discretization: (Jn_{i+1/2}-Jn_{i-1/2}) = q*R_SRH*dx
        % Jn_{i+1/2} = q*Dn/dx * [ n_{i+1}*B(dpsi) - n_i*B(-dpsi) ], dpsi=(fi(i+1)-fi(i))
        A = zeros(N,1); Bm = zeros(N,1); Cc = zeros(N,1); rhs = zeros(N,1);
        % SRH recombination evaluated at previous (lagged) values for linearity
        R_SRH = srh_rate(n, p, ni, TAUN0, TAUP0);  % [cm^-3 s^-1]

        for i = 2:N-1
            dpsi_f = fi(i+1)-fi(i);
            dpsi_b = fi(i)-fi(i-1);
            a_i = (Dn/dx2)*berfun(dpsi_b);
            c_i = (Dn/dx2)*berfun(-dpsi_f);
            b_i = -(a_i + c_i);
            A(i)  = a_i;
            Bm(i) = b_i;
            Cc(i) = c_i;
            rhs(i)= -R_SRH(i);  % bring to RHS
        end
        % Dirichlet for n
        Bm(1)=1; rhs(1)=nL; A(1)=0; Cc(1)=0;
        Bm(N)=1; rhs(N)=nR; A(N)=0; Cc(N)=0;

        n = LU_Decomposition(A,Bm,Cc,rhs,N);

        % --------------------- (3) Solve hole continuity -----------------------
        % Jp_{i+1/2} = -q*Dp/dx * [ p_{i+1}*B(-dpsi) - p_i*B(dpsi) ]
        A = zeros(N,1); Bm = zeros(N,1); Cc = zeros(N,1); rhs = zeros(N,1);
        for i = 2:N-1
            dpsi_f = fi(i+1)-fi(i);
            dpsi_b = fi(i)-fi(i-1);
            a_i = (Dp/dx2)*berfun(-dpsi_b);
            c_i = (Dp/dx2)*berfun(dpsi_f);
            b_i = -(a_i + c_i);
            A(i)  = a_i;
            Bm(i) = b_i;
            Cc(i) = c_i;
            rhs(i)= -R_SRH(i);  % same SRH (trap at Ei)
        end
        % Dirichlet for p
        Bm(1)=1; rhs(1)=pL; A(1)=0; Cc(1)=0;
        Bm(N)=1; rhs(N)=pR; A(N)=0; Cc(N)=0;

        p = LU_Decomposition(A,Bm,Cc,rhs,N);

        % ---------------------------- Convergence ------------------------------
        % Relative updates to avoid scale issues
        rel_n = max(abs((n - n_old)./max(n,1)));
        rel_p = max(abs((p - p_old)./max(p,1)));
        rel_f = max(abs(fi - fi_old));
        if max([rel_n, rel_p, rel_f]) < tol_inner
            break;
        end
        if it==max_iter
            warning('Gummel did not fully converge at VA=%.4f V (max rel=%.3e).', VA, max([rel_n,rel_p,rel_f]));
        end
    end

    % Save equilibrium snapshot
    if kv == 1   % this is VA = 0 (equilibrium)
        fi_eq = fi; n_eq = n; p_eq = p;
    end

    %% -------------- Compute terminal current density (A/cm^2) ---------------
    % SG currents (should be nearly constant across device)
    Jn = zeros(N-1,1);
    Jp = zeros(N-1,1);
    for i = 1:N-1
        dpsi = fi(i+1)-fi(i);
        Jn(i) =  q*Dn/dx*( n(i+1)*berfun(dpsi) - n(i)*berfun(-dpsi) );
        Jp(i) = -q*Dp/dx*( p(i+1)*berfun(-dpsi) - p(i)*berfun( dpsi) );
    end
    J_total(kv) = mean(Jn + Jp);  % near-constant; use mean for robustness

    % Store/plot intermediate profiles at selected biases if desired
    % (commented: uncomment to inspect)
    % if abs(VA-0.0)<1e-12 || abs(VA-0.6)<1e-12 || abs(VA-0.8)<1e-12
    %     figure; semilogy(x*1e4, n, x*1e4, p); grid on;
    %     xlabel('x [\mum]'); ylabel('Carrier density [cm^{-3}]');
    %     legend('n','p'); title(sprintf('Carrier profiles at V_A=%.3f V',VA));
    % end
end

% ------------------ One-off targeted solve at VA = 0.75 V ------------------
VA = 0.75;                       % [V]
% Ohmic contacts with injected minorities at 0.75 V
nL = Nd;                         % majority on n-contact
pL = (ni^2/Nd)*exp(VA/Vt);       % injected holes on n-contact
pR = Na;                         % majority on p-contact
nR = (ni^2/Na)*exp(VA/Vt);       % injected electrons on p-contact

% Dirichlet potentials from carrier BC (EF,eq is reference -> same convention)
fiL = log(nL/ni);
fiR = log(nR/ni);

% Start from most recent solution for faster convergence
% (fi, n, p already exist from the sweep; they're good initial guesses)
for it = 1:max_iter
    n_old = n; p_old = p; fi_old = fi;

    % ---- Poisson (linearized, same as in your loop) ----
    dx2 = dx*dx;
    a = zeros(N,1); b = zeros(N,1); c = zeros(N,1); f = zeros(N,1);
    for i = 2:N-1
        a(i) = 1/dx2; c(i) = 1/dx2;
        b(i) = -(2/dx2 + exp(fi(i)) + exp(-fi(i)));
        f(i) =  (exp(fi(i)) - exp(-fi(i)) - dop(i)) ...
               - fi(i)*(exp(fi(i)) + exp(-fi(i)));
    end
    b(1)=1; f(1)=fiL; b(N)=1; f(N)=fiR;

    for ip = 1:max_poi
        fi_new = LU_Decomposition(a,b,c,f,N);
        if max(abs(fi_new - fi)) < tol_poi
            fi = fi_new; break;
        end
        fi = fi_new;
        for i = 2:N-1
            b(i) = -(2/dx2 + exp(fi(i)) + exp(-fi(i)));
            f(i) =  (exp(fi(i)) - exp(-fi(i)) - dop(i)) ...
                   - fi(i)*(exp(fi(i)) + exp(-fi(i)));
        end
        f(1)=fiL; f(N)=fiR;
    end

    % Update carriers from potential (good Gummel seed)
    n = ni*exp(fi); p = ni*exp(-fi);
    % Enforce Dirichlet carrier BCs (ohmic)
    n(1)=nL; p(1)=pL; n(N)=nR; p(N)=pR;

    % ---- Electron continuity (SG) ----
    A = zeros(N,1); Bm = zeros(N,1); Cc = zeros(N,1); rhs = zeros(N,1);
    R_SRH = srh_rate(n, p, ni, TAUN0, TAUP0);
    for i = 2:N-1
        dpsi_f = fi(i+1)-fi(i);
        dpsi_b = fi(i)-fi(i-1);
        a_i = (Dn/dx2)*berfun(dpsi_b);
        c_i = (Dn/dx2)*berfun(-dpsi_f);
        A(i)=a_i; Cc(i)=c_i; Bm(i)=-(a_i+c_i);
        rhs(i) = -R_SRH(i);
    end
    Bm(1)=1; rhs(1)=nL; A(1)=0; Cc(1)=0;
    Bm(N)=1; rhs(N)=nR; A(N)=0; Cc(N)=0;
    n = LU_Decomposition(A,Bm,Cc,rhs,N);

    % ---- Hole continuity (SG) ----
    A = zeros(N,1); Bm = zeros(N,1); Cc = zeros(N,1); rhs = zeros(N,1);
    for i = 2:N-1
        dpsi_f = fi(i+1)-fi(i);
        dpsi_b = fi(i)-fi(i-1);
        a_i = (Dp/dx2)*berfun(-dpsi_b);
        c_i = (Dp/dx2)*berfun(dpsi_f);
        A(i)=a_i; Cc(i)=c_i; Bm(i)=-(a_i+c_i);
        rhs(i) = -R_SRH(i);
    end
    Bm(1)=1; rhs(1)=pL; A(1)=0; Cc(1)=0;
    Bm(N)=1; rhs(N)=pR; A(N)=0; Cc(N)=0;
    p = LU_Decomposition(A,Bm,Cc,rhs,N);

    % Convergence check
    rel_n = max(abs((n - n_old)./max(n,1)));
    rel_p = max(abs((p - p_old)./max(p,1)));
    rel_f = max(abs(fi - fi_old));
    if max([rel_n, rel_p, rel_f]) < tol_inner
        break;
    end
end

% Save snapshot at VA = 0.75 V
fi_075 = fi; n_075 = n; p_075 = p;

% ===================== Current conservation at VA = 0.75 V =====================
% SG midpoint currents across the device (should be ~constant)
Jn_075 = zeros(N-1,1);
Jp_075 = zeros(N-1,1);
x_mid  = (x(1:end-1) + x(2:end))/2;   % midpoints for current locations

for i = 1:N-1
    dpsi = fi_075(i+1) - fi_075(i);   % dimensionless potential drop
    % Electron and hole currents (Scharfetter–Gummel)
    Jn_075(i) =  q*Dn/dx * (  n_075(i+1)*berfun( dpsi) - n_075(i)*berfun(-dpsi) );
    Jp_075(i) = -q*Dp/dx * (  p_075(i+1)*berfun(-dpsi) - p_075(i)*berfun( dpsi) );
end
Jtot_075 = Jn_075 + Jp_075;

% Report constancy (max deviation across device)
J_span   = max(Jtot_075) - min(Jtot_075);
J_mean   = mean(Jtot_075);
rel_deviation = J_span / max(1e-30, abs(J_mean));   % dimensionless

fprintf('VA=0.75 V: <J> = %.4e A/cm^2, span = %.4e, relative deviation = %.3e\n', ...
        J_mean, J_span, rel_deviation);

% Optional: discrete continuity residual check (steady state: dJ/dx + q*R = 0)
R_SRH_075 = srh_rate(n_075, p_075, ni, TAUN0, TAUP0); % [cm^-3 s^-1]
residual  = zeros(N-2,1);
for i = 2:N-1
    dJdx = (Jtot_075(i) - Jtot_075(i-1)) / dx;
    residual(i-1) = dJdx + q*R_SRH_075(i);  % should be ~0
end
fprintf('Continuity residual (VA=0.75 V): max|dJ/dx+qR| = %.4e\n', max(abs(residual)));

% Plot current profiles to visually confirm conservation
figure('Color','w');
plot(x_mid*1e4, Jn_075, 'LineWidth', 1.8); hold on;
plot(x_mid*1e4, Jp_075, 'LineWidth', 1.8);
plot(x_mid*1e4, Jtot_075, 'k', 'LineWidth', 2.0); grid on; hold off;
xlabel('x [\mu m]');
ylabel('Current density [A/cm^2]');
title('Current conservation at V_A = 0.75 V');
legend('J_n','J_p','J_{total}','Location','best');

%% --------------------------------- Plots ----------------------------------
% I–V in A/cm^2 (1D => per-unit-area current)
figure('Color','w');
plot(Vlist, J_total, 'LineWidth', 2); grid on;
xlabel('Anode Bias V_A [V]');
ylabel('Current Density J [A/cm^2]');
title('PN Diode I–V (Drift–Diffusion, SG, Gummel)');  % en dash

figure('Color','w');
semilogy(Vlist, abs(J_total)+eps, 'LineWidth', 2); grid on;
xlabel('Anode Bias V_A [V]');
ylabel('|\itJ| [A/cm^2] (semilog)');
title('PN Diode I–V (semilog)');

% --------------------- Band edges & density comparison ---------------------
x_um = x*1e4;                  % position in micrometers

% Equilibrium band edges (E_F,eq is reference 0 eV)
Ec_eq = dEc - Vt*fi_eq;        % [eV]
Ev_eq = Ec_eq - Eg;            % [eV]

% Biased band edges at VA = 0.75 V
Ec_075 = dEc - Vt*fi_075;      % [eV]
Ev_075 = Ec_075 - Eg;          % [eV]

% ================= Quasi-Fermi levels at VA = 0.75 V =================
% Derive Nv from ni, Nc, Eg (at 300K)
RNv = (ni^2 / RNc) * exp(Eg / Vt);    % [cm^-3]

% Quasi-Fermi levels relative to equilibrium EF reference (0 eV)
EFn_075 = Ec_075 + Vt*log( max(n_075,1) ./ RNc );   % [eV]
EFp_075 = Ev_075 - Vt*log( max(p_075,1) ./ RNv );   % [eV]

% (A) Conduction & valence bands: equilibrium vs 0.75 V
figure('Color','w');
plot(x_um, Ec_eq, 'LineWidth', 1.8); hold on;
plot(x_um, Ev_eq, 'LineWidth', 1.8);
plot(x_um, Ec_075, '--', 'LineWidth', 1.8);
plot(x_um, Ev_075, '--', 'LineWidth', 1.8); grid on; hold off;
xlabel('x [\mu m]');
ylabel('Energy [eV]');
title('Conduction and Valence Band Edges: Equilibrium vs. V_A = 0.75 V');
legend('E_c (eq)','E_v (eq)','E_c (0.75 V)','E_v (0.75 V)','Location','best');

% (B) Electron & hole densities: equilibrium vs 0.75 V
figure('Color','w');
semilogy(x_um, n_eq, 'LineWidth', 1.8); hold on;
semilogy(x_um, p_eq, 'LineWidth', 1.8);
semilogy(x_um, n_075, '--', 'LineWidth', 1.8);
semilogy(x_um, p_075, '--', 'LineWidth', 1.8); grid on; hold off;
xlabel('x [\mu m]');
ylabel('Carrier Density [cm^{-3}]');
title('n(x) and p(x): Equilibrium vs. V_A = 0.75 V');
legend('n (eq)','p (eq)','n (0.75 V)','p (0.75 V)','Location','best');

% Plot quasi-Fermi levels with the band edges for context
figure('Color','w');
plot(x_um, Ec_075, 'LineWidth', 1.6); hold on;
plot(x_um, Ev_075, 'LineWidth', 1.6);
plot(x_um, EFn_075, '--', 'LineWidth', 1.8);
plot(x_um, EFp_075, '--', 'LineWidth', 1.8); grid on; hold off;
xlabel('x [\mu m]');
ylabel('Energy [eV]');
title('Quasi-Fermi Levels at V_A = 0.75 V (reference: E_{F,eq} = 0)');
legend('E_c','E_v','E_{Fn}','E_{Fp}','Location','best');

%% ------------------------------- Subfunctions -----------------------------
function R = srh_rate(n, p, ni, taun, taup)
    % SRH with trap at intrinsic level:
    % R = (np - ni^2) / ( taup*(n+ni) + taun*(p+ni) )
    R = (n.*p - ni^2) ./ ( taup*(n + ni) + taun*(p + ni) );
end

function [output] = LU_Decomposition(a,b,c,f,n_max)
    % Tridiagonal LU (absorbed style)
    d = zeros(n_max,1); v = zeros(n_max,1); output = zeros(n_max,1);
    d(1) = b(1);
    for i = 2:n_max
        d(i) = b(i) - a(i)*c(i-1)/d(i-1);
    end
    v(1) = f(1);
    for i = 2:n_max
        v(i) = f(i) - a(i)*v(i-1)/d(i-1);
    end
    output(n_max) = v(n_max)/d(n_max);
    for i = n_max-1:-1:1
        output(i) = (v(i)-c(i)*output(i+1))/d(i);
    end
end

function Ber = berfun(x)
    % Bernoulli function with robust small-argument handling (absorbed)
    flag_conv = 0;
    if (x > 0.01)
        Ber = x*exp(-x)/(1-exp(-x));
    elseif (x < 0 && abs(x) > 0.01)
        Ber = x/(exp(x)-1);
    elseif (x == 0)
        Ber = 1;
    else
        temp_term = 1; sumv = temp_term; i = 0;
        while(~flag_conv)
            i = i + 1;
            temp_term = temp_term*x/(i+1);
            if (sumv + temp_term == sumv), flag_conv = 1; end
            sumv = sumv + temp_term;
        end
        Ber = 1/sumv;
    end
end

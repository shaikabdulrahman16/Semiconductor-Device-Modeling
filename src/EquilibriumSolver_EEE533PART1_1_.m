function [output] = LU_Decomposition(a,b,c,f,n_max)

    d = zeros(n_max,1);
    v = zeros(n_max,1);
    
    d(1) = b(1);
    for i = 2: n_max
        d(i) = b(i) - a(i)*c(i-1)/d(i-1);
    end

    % Solution of Lv = f %

    v(1) = f(1);
    for i = 2: n_max
        v(i) = f(i) - a(i)*v(i-1)/d(i-1)  ;
    end

    % Solution of U*fi = v %

    output(n_max) = v(n_max)/d(n_max);
    for i = n_max-1:-1:1
        output(i) = (v(i)-c(i)*output(i+1))/d(i);
    end
    
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function Ber = berfun(x)
flag_conv = 0;
          if(x>0.01)
             Ber = x*exp(-x)/(1-exp(-x));
          elseif(x<0 && abs(x)> 0.01)
              Ber = x/(exp(x)-1);
          elseif(x == 0)
             Ber = 1;
          else
             temp_term = 1;
             sum = temp_term;
             i = 0;
             while(~flag_conv)
                i = i + 1;
                temp_term = temp_term*x/(i+1);
                if( sum + temp_term == sum)
                    flag_conv = 1;
                end
                sum = sum + temp_term;
             end
             Ber = 1/sum;
          end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                                                                         %%
%%             Equilibrium Poisson Equation Solver for Diodes              %%
%%                                                                         %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;

% Defining the Fundamental and Material Constants %

q   = 1.602E-19;
kb  = 1.38E-23;
eps = 1.05E-12;
T   = 300;
ni  = 1.5E10;
Vt  = kb*T/q;
RNc = 2.8E19;
dEc = Vt*log(RNc/ni);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 1 batch runner (3 cases) %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Fundamental / material constants
q   = 1.602E-19;
kb  = 1.38E-23;
eps = 1.05E-12;
T   = 300;
ni  = 1.5E10;
Vt  = kb*T/q;
RNc = 2.8E19;
dEc = Vt*log(RNc/ni);

delta_acc = 1E-9;   % Poisson convergence tolerance

% ----- The three requested cases -----
cases = {
    struct('Nd',1e15,'Na',1e16,'label','(a) Nd=1e15, Na=1e16','tag','a')
    struct('Nd',1e17,'Na',1e17,'label','(b) Nd=1e17, Na=1e17','tag','b')
    struct('Nd',1e17,'Na',1e18,'label','(c) Nd=1e17, Na=1e18','tag','c')
};

% To avoid a "short diode", choose each side length as a multiple of its
% depletion extent from the depletion approximation.
safety_mult = 8;  % increase to 8–10 if you want extra margin

for k = 1:numel(cases)

    % --------------------------
    % (1) Pick doping and size
    % --------------------------
    Nd = cases{k}.Nd;           % [cm^-3]
    Na = cases{k}.Na;           % [cm^-3]

    % Built-in and depletion widths (depletion approximation)
    Vbi = Vt * log( (Na*Nd)/(ni^2) );
    W   = sqrt( 2*eps/q * (1/Na + 1/Nd) * Vbi );   % total width [cm]
    Wp  = W * Nd/(Na+Nd);                          % into p-side [cm]
    Wn  = W * Na/(Na+Nd);                          % into n-side [cm]

    % Region lengths so it's NOT a short diode
    x_n = safety_mult * Wn;    % [cm]
    x_p = safety_mult * Wp;    % [cm]

    % --------------------------
    % (2) Set up grid (your way)
    % --------------------------
Ldn = sqrt(eps*Vt/(q*Nd));
Ldp = sqrt(eps*Vt/(q*Na));
Ldi = sqrt(eps*Vt/(q*ni));

x_max = x_n + x_p;

dx = Ldn;
    if (dx > Ldp), dx = Ldp; end
dx = dx/5;

    n_max = round(x_max/dx);
    dx = dx/Ldi;     % normalize by Ldi

    % --------------------------
    % (3) Allocate arrays
    % --------------------------
dop = zeros(n_max,1);
fi  = zeros(n_max,1);
fip = zeros(n_max,1);
n   = zeros(n_max,1);
p   = zeros(n_max,1);
a   = zeros(n_max,1);
b   = zeros(n_max,1);
c   = zeros(n_max,1);
d   = zeros(n_max,1);
f   = zeros(n_max,1);
v   = zeros(n_max,1);
Ec   = zeros(n_max,1);
el_field   = zeros(n_max,1);
ro   = zeros(n_max,1);
xx1 = zeros(n_max,1);
delta_vec = zeros(n_max,1);

    % --------------------------
    % (4) Doping profile (Nd - Na), normalized by ni
    % --------------------------
for i = 1:n_max
        xxx = i*dx*Ldi;     % back to [cm]
        if (xxx <= x_n)
        dop(i) = Nd/ni;
        else
        dop(i) = -Na/ni;
    end
end

    % --------------------------
    % (5) Initial guess (charge neutrality)
    % --------------------------
    for i = 1:n_max
    zz = 0.5*dop(i);
        if (zz > 0)
        xx = zz*(1 + sqrt(1+1/(zz*zz)));
        elseif (zz < 0)
        xx = zz*(1 - sqrt(1+1/(zz*zz)));
        else
            xx = 1;
        end
        fi(i) = log(xx);
        n(i)  = xx;
        p(i)  = 1/xx;
    end

    % --------------------------
    % (6) Linearized Poisson (your formulation)
    % --------------------------
dx2 = dx*dx;
    for i = 2:n_max-1
    a(i) = 1/dx2;
    c(i) = 1/dx2;
    b(i) = -(2/dx2+exp(fi(i))+exp(-fi(i)));
    f(i) = exp(fi(i))-exp(-fi(i))-dop(i) - fi(i)*(exp(fi(i))+exp(-fi(i)));
end

    % Ohmic contacts (Dirichlet)
    a(1)=0; c(1)=0; b(1)=1;       f(1)=fi(1);
    a(n_max)=0; c(n_max)=0; b(n_max)=1; f(n_max)=fi(n_max);

    % --------------------------
    % (7) Iteration
    % --------------------------
    flag_conv = 0;
    while (~flag_conv)
        fip = LU_Decomposition(a,b,c,f,n_max);

        delta_max = max(abs(fip - fi));
        if (delta_max < delta_acc)
        flag_conv = 1;
    else
            for i = 2:n_max-1
            b(i) = -(2/dx2+exp(fip(i))+exp(-fip(i)));
            f(i) = exp(fip(i))-exp(-fip(i))-dop(i)-fip(i)*(exp(fip(i))+exp(-fip(i)));
    end
    fi = fip;
        end
    end

    % --------------------------
    % (8) Back to physical units, field, etc.
    % --------------------------
for i = 1:n_max
        Ec(i) = dEc - Vt*fi(i);         % [eV]
        n(i)  = ni*exp(fi(i));          % [cm^-3]
        p(i)  = ni*exp(-fi(i));         % [cm^-3]
        ro(i) = q*(p(i) - n(i) + ni*dop(i));   % [C/cm^3]
    end

    xx1(1) = dx*Ldi*1e4; % [um]
for i = 2:n_max-1
        xx1(i) = xx1(i-1) + dx*Ldi*1e4;
        el_field(i) = -(fi(i+1) - fi(i-1)) * Vt /(2 * dx * Ldi); % [V/cm]
    end
    xx1(n_max)   = xx1(n_max-1) + dx*Ldi*1e4;
    el_field(1)  = el_field(2);
    el_field(end)= el_field(end-1);

    % --------------------------
    % (9) Extract E_peak and depletion width W from E(x)
    % --------------------------
    [Epk_val, Epk_idx] = max(abs(el_field));
    Epk = el_field(Epk_idx);               % signed peak [V/cm]
    x_Epk = xx1(Epk_idx);                  % location [um]

    % define depletion region from field profile: |E| >= 1% of |E|max
    thr = 0.01 * Epk_val;
    idxs = find(abs(el_field) >= thr);

    % total depletion width from field profile [um]
    W_um = xx1(max(idxs)) - xx1(min(idxs));

    % split around the metallurgical junction at x = x_n
    x_n_um = x_n*1e4;
    i_junc = find(xx1 >= x_n_um, 1, 'first');

    % n-side and p-side extents (approx) [um]
    Wn_um = x_n_um - xx1(min(idxs(idxs<=i_junc)));
    Wp_um = xx1(max(idxs(idxs>=i_junc))) - x_n_um;

    % print to console for your report
    fprintf('\n=== %s ===\n', cases{k}.label);
    fprintf('Chosen region lengths (not short): x_n = %.3f um, x_p = %.3f um (safety x%d)\n', x_n*1e4, x_p*1e4, safety_mult);
    fprintf('E_peak = %.3e V/cm at x = %.3f um\n', Epk, x_Epk);
    fprintf('Depletion width from field (|E| >= 1%% max): W = %.3f um  [Wn ~ %.3f, Wp ~ %.3f]\n', W_um, Wn_um, Wp_um);

    % --------------------------
    % (9b) Depletion-approx (DA) vs Simulation: Vbi, W, Emax
    % --------------------------
    % DA (analytical, abrupt junction)
    Vbi_DA = Vt * log( (Na*Nd)/(ni^2) );                         % [V]
    W_DA   = sqrt( 2*eps/q * (1/Na + 1/Nd) * Vbi_DA );           % [cm]
    Wn_DA  = W_DA * Na/(Na+Nd);                                  % [cm]
    Wp_DA  = W_DA * Nd/(Na+Nd);                                  % [cm]
    Emax_DA = q * Nd * Wn_DA / eps;                              % [V/cm] (== q*Na*Wp_DA/eps)

    % Simulation-based built-in potential (use a tiny average at the ends for stability)
    avgN = min(5, floor(n_max/10));  % average over a few nodes; safe even for small meshes
    fi_left  = mean(fi(1:avgN));     
    fi_right = mean(fi(end-avgN+1:end));
    Vbi_sim  = Vt * (fi_right - fi_left);                        % [V]

    % Report & percent differences (sim - DA)/DA
    W_DA_um = W_DA * 1e4;    % [um]
    Wn_DA_um = Wn_DA * 1e4;  % [um]
    Wp_DA_um = Wp_DA * 1e4;  % [um]

    dVbi_pct = 100*(Vbi_sim - Vbi_DA)/Vbi_DA;
    dEmax_pct = 100*(abs(Epk) - Emax_DA)/Emax_DA;
    dW_pct    = 100*(W_um - W_DA_um)/W_DA_um;

    fprintf('--- Depletion Approx vs Simulation ( %s ) ---\n', cases{k}.label);
    fprintf('DA:  Vbi=%.3f V,  W=%.3f um  [Wn=%.3f, Wp=%.3f],  Emax=%.3e V/cm\n', ...
            Vbi_DA, W_DA_um, Wn_DA_um, Wp_DA_um, Emax_DA);
    fprintf('Sim: Vbi=%.3f V,  W=%.3f um,                     Epeak=%.3e V/cm\n', ...
            Vbi_sim, W_um, abs(Epk));
    fprintf('Diff (Sim-DA)/DA:  dVbi=%.1f%%,  dW=%.1f%%,  dEmax=%.1f%%\n\n', ...
            dVbi_pct, dW_pct, dEmax_pct);

    % --------------------------
    % (10) Plots (required & labeled) - Save to Project results folder
    % --------------------------
    
    % Create Project results folder if it doesn't exist
    if ~exist('Project results', 'dir')
        mkdir('Project results');
    end

    % 1) Energy band diagram (Ec & Ev)
    figure('Name',['Bands ',cases{k}.label], 'Visible', 'off'); 
    plot(xx1, Ec, 'LineWidth',1.4); hold on;
    plot(xx1, Ec - 1.12, 'LineWidth',1.2);      % Ev ≈ Ec - Eg (Eg≈1.12 eV at 300K)
    yline(0,'k-','E_i \approx 0','LabelHorizontalAlignment','left');
    xline(x_n_um,'--','Junction','LabelVerticalAlignment','middle');
    xlabel('x [\mum]'); ylabel('Energy [eV]');
    title(['Conduction & Valence Bands vs Position ', cases{k}.label]);
    legend('E_c','E_v','Location','best'); grid on;
    saveas(gcf, sprintf('Project results/case_%s_bands.png', cases{k}.tag));
    close(gcf);

    % 2) Electric field (with E_peak & shaded depletion region)
    figure('Name',['Electric Field ',cases{k}.label], 'Visible', 'off');
    plot(xx1, el_field, 'LineWidth',1.4); hold on;
    xline(x_n_um,'--','Junction');
    % shade depletion region (where |E| >= 1% of max)
    x_depl = xx1([min(idxs) max(idxs)]);
    yL = min(el_field); yU = max(el_field);
    patch([x_depl(1) x_depl(2) x_depl(2) x_depl(1)], [yL yL yU yU], ...
          [0.9 0.9 1.0], 'FaceAlpha',0.2, 'EdgeColor','none'); %#ok<NBRAK>
    plot(x_Epk, Epk, 'o', 'MarkerSize',6, 'LineWidth',1.2);
    text(x_Epk, Epk, sprintf('  E_{peak}=%.2e V/cm',Epk), 'VerticalAlignment','bottom');
    xlabel('x [\mum]'); ylabel('Electric Field [V/cm]');
    title(['Electric Field vs Position ', cases{k}.label]);
    legend('E profile','Junction','Depletion region','E_{peak}','Location','best'); grid on;
    saveas(gcf, sprintf('Project results/case_%s_field.png', cases{k}.tag));
    close(gcf);

    % 3) Electron & hole densities (semilog)
    figure('Name',['Carrier Densities ',cases{k}.label], 'Visible', 'off');
    semilogy(xx1, n, 'LineWidth',1.4); hold on;
    semilogy(xx1, p, 'LineWidth',1.4);
    xline(x_n_um,'--','Junction');
    xlabel('x [\mum]'); ylabel('Carrier Density [cm^{-3}]');
    title(['Electron & Hole Densities vs Position ', cases{k}.label]);
    legend('n','p','Junction','Location','best'); grid on;
    saveas(gcf, sprintf('Project results/case_%s_carriers.png', cases{k}.tag));
    close(gcf);

    % 4) Total charge density
    figure('Name',['Total Charge ',cases{k}.label], 'Visible', 'off');
    ro_plot = ro; ro_plot(1)=ro_plot(2); ro_plot(end)=ro_plot(end-1);
    plot(xx1, ro_plot, 'LineWidth',1.4); hold on;
    xline(x_n_um,'--','Junction');
    xlabel('x [\mum]'); ylabel('Total Charge Density [C/cm^3]');
    title(['Total Charge Density vs Position ', cases{k}.label]);
    legend('\rho_{tot}','Junction','Location','best'); grid on;
    saveas(gcf, sprintf('Project results/case_%s_charge.png', cases{k}.tag));
    close(gcf);

    % --------------------------
    % (11) (Optional) Save per-case arrays without overwriting
    % --------------------------
    % save(sprintf('cond_band_%s.mat',cases{k}.tag), 'xx1','Ec');
    % save(sprintf('electric_field_%s.mat',cases{k}.tag), 'xx1','el_field');
    % save(sprintf('np_data_%s.mat',cases{k}.tag), 'xx1','n','p');
    % save(sprintf('tot_charge_%s.mat',cases{k}.tag), 'xx1','ro');
    % save(sprintf('pot_%s.mat',cases{k}.tag), 'fi');

    % --------------------------
    % (12) Print numeric results for report
    % --------------------------
    % (Results already printed in section 9)

end

% --------------------------
% Summary message
% --------------------------
fprintf('\n=== Analysis Complete ===\n');
fprintf('All plots saved to "Project results" folder:\n');
fprintf('- Energy band diagrams: case_a_bands.png, case_b_bands.png, case_c_bands.png\n');
fprintf('- Electric field profiles: case_a_field.png, case_b_field.png, case_c_field.png\n');
fprintf('- Carrier densities: case_a_carriers.png, case_b_carriers.png, case_c_carriers.png\n');
fprintf('- Total charge density: case_a_charge.png, case_b_charge.png, case_c_charge.png\n');
function ENIT_Aero_Dashboard()
    % =====================================================================
    % PROJET : SIMULATEUR DE CONTRÔLE MLI AVANCÉ
    % INSTITUTION : ECOLE NATIONALE D'INGÉNIEURS DE TUNIS (ENIT)
    % RÉALISATEURS : WAEL GUESMI & MAHA ROMDHANI
    % ENCADRANT : MR. KHALED JLASSI
    % =====================================================================

    % --- PARAMÈTRES DE SIMULATION ---
    fs = 500000;                % Fréquence d'échantillonnage ultra-haute
    t_scope = 0:1/fs:0.0012;    % Fenêtre temporelle pour 1k-10k Hz
    f_val = 1000;               % Fréquence initiale
    d_val = 0;                  % Duty cycle initial
    angle_motor = 0;            % Angle de rotation initial

    % --- CRÉATION DE LA FIGURE PRINCIPALE ---
    fig = figure('Name', 'MLI | ETUDE THEORIQUE ', ...
                 'NumberTitle', 'off', 'Color', [0.03 0.04 0.06], ...
                 'Units', 'normalized', 'Position', [0.05 0.05 0.9 0.85], ...
                 'MenuBar', 'none', 'ToolBar', 'none');

    % --- DESIGN DU HEADER (ENTÊTE) ---
    header_panel = uipanel('Parent', fig, 'Units', 'normalized', ...
                           'Position', [0 0.88 1 0.12], 'BackgroundColor', [0.05 0.07 0.1], ...
                           'BorderType', 'none');

    uicontrol('Parent', header_panel, 'Style', 'text', 'String', 'ENIT - DÉPARTEMENT GÉNIE ÉLECTRIQUE', ...
              'Units', 'normalized', 'Position', [0.02 0.5 0.4 0.4], ...
              'FontSize', 18, 'FontWeight', 'bold', 'ForegroundColor', [0 0.8 1], ...
              'BackgroundColor', [0.05 0.07 0.1], 'HorizontalAlignment', 'left');

    uicontrol('Parent', header_panel, 'Style', 'text', 'String', 'PROJET : GENERATION DE  SIGNAL  MLI', ...
              'Units', 'normalized', 'Position', [0.02 0.1 0.4 0.3], ...
              'FontSize', 11, 'ForegroundColor', [1 1 1], ...
              'BackgroundColor', [0.05 0.07 0.1], 'HorizontalAlignment', 'left');

    % --- ZONE RÉALISATEURS ET ENCADRANT ---
    info_panel = uipanel('Parent', fig, 'Units', 'normalized', ...
                         'Position', [0.75 0.88 0.25 0.12], 'BackgroundColor', [0.05 0.07 0.1], ...
                         'BorderType', 'none');

    uicontrol('Parent', info_panel, 'Style', 'text', 'String', 'Réalisé par :', ...
              'Units', 'normalized', 'Position', [0 0.7 0.9 0.2], ...
              'FontSize', 9, 'ForegroundColor', [0.6 0.6 0.6], 'BackgroundColor', [0.05 0.07 0.1]);

    uicontrol('Parent', info_panel, 'Style', 'text', 'String', 'WAEL GUESMI & MAHA ROMDHANI', ...
              'Units', 'normalized', 'Position', [0 0.45 0.9 0.25], ...
              'FontSize', 10, 'FontWeight', 'bold', 'ForegroundColor', [1 1 1], 'BackgroundColor', [0.05 0.07 0.1]);

    uicontrol('Parent', info_panel, 'Style', 'text', 'String', 'ENCADREE PAR  : MR. KHALED JLASSI', ...
              'Units', 'normalized', 'Position', [0 0.1 0.9 0.25], ...
              'FontSize', 10, 'FontWeight', 'bold', 'ForegroundColor', [1 0.8 0], 'BackgroundColor', [0.05 0.07 0.1]);

    % --- ZONE CENTRALE : OSCILLOSCOPE ---
    ax_scope = axes('Parent', fig, 'Units', 'normalized', 'Position', [0.35 0.35 0.6 0.48], ...
                   'Color', [0 0 0], 'XColor', [0.2 0.5 0.5], 'YColor', [0.2 0.5 0.5], ...
                   'GridAlpha', 0.2, 'MinorGridAlpha', 0.1);
    grid(ax_scope, 'on'); hold(ax_scope, 'on');
    hPlot = plot(ax_scope, t_scope, zeros(size(t_scope)), 'Color', [0 1 0.5], 'LineWidth', 2.5);
    ylim(ax_scope, [-0.1 1.1]);
    ylabel(ax_scope, 'Amplitude (V)'); xlabel(ax_scope, 'Temps (s)');

    % --- ZONE MOTEUR (ANIMATION) ---
    ax_motor = axes('Parent', fig, 'Units', 'normalized', 'Position', [0.05 0.45 0.25 0.35], ...
                    'Color', 'none', 'XColor', 'none', 'YColor', 'none');
    hold(ax_motor, 'on');
    rectangle('Position', [-0.9 -0.9 1.8 1.8], 'Curvature', [1 1], 'EdgeColor', [0.1 0.3 0.5], 'LineWidth', 3);
    hProp = fill([-0.8 0.8 0.04 -0.04], [0.04 0.04 -0.04 -0.04], [0.8 0.8 0.8], 'EdgeColor', 'none');
    hProp2 = fill([0.04 0.04 -0.04 -0.04], [-0.8 0.8 0.04 -0.04], [0.8 0.8 0.8], 'EdgeColor', 'none');
    axis(ax_motor, 'equal'); xlim(ax_motor, [-1 1]); ylim(ax_motor, [-1 1]);

    % --- ZONE LEDS D'ÉTAT ---
    led_panel = uipanel('Parent', fig, 'Title', ' SYTEM LOAD MONITOR ', 'Units', 'normalized', ...
                        'Position', [0.35 0.2 0.6 0.12], 'BackgroundColor', [0.05 0.05 0.08], ...
                        'ForegroundColor', 'white');
    ax_leds = axes('Parent', led_panel, 'Units', 'normalized', 'Position', [0.05 0.1 0.9 0.8], ...
                   'Color', 'none', 'XColor', 'none', 'YColor', 'none');
    hold(ax_leds, 'on');
    leds_h(1) = rectangle('Position', [1 0.1 0.8 0.8], 'Curvature', [1 1], 'FaceColor', [0.1 0.1 0.1], 'EdgeColor', 'none');
    leds_h(2) = rectangle('Position', [3 0.1 0.8 0.8], 'Curvature', [1 1], 'FaceColor', [0.1 0.1 0.1], 'EdgeColor', 'none');
    leds_h(3) = rectangle('Position', [5 0.1 0.8 0.8], 'Curvature', [1 1], 'FaceColor', [0.1 0.1 0.1], 'EdgeColor', 'none');
    axis(ax_leds, 'equal'); xlim(ax_leds, [0 7]);

    % --- ZONE DE CONTRÔLE (KNOBS / CURSEURETTES) ---
    ctrl_panel = uipanel('Parent', fig, 'Units', 'normalized', ...
                         'Position', [0.05 0.02 0.9 0.15], 'BackgroundColor', [0.08 0.1 0.15], ...
                         'BorderType', 'etchedin');

    % Knob pour la Fréquence
    uicontrol('Parent', ctrl_panel, 'Style', 'text', 'String', 'FRÉQUENCE (Hz)', ...
              'Units', 'normalized', 'Position', [0.05 0.1 0.1 0.3], 'BackgroundColor', [0.08 0.1 0.15], 'ForegroundColor', 'white');
    k_freq = uicontrol('Parent', ctrl_panel, 'Style', 'slider', 'Units', 'normalized', ...
                       'Position', [0.15 0.4 0.25 0.3], 'Min', 1000, 'Max', 10000, 'Value', 1000);
    txt_freq_val = uicontrol('Parent', ctrl_panel, 'Style', 'text', 'String', '1000 Hz', ...
                            'Units', 'normalized', 'Position', [0.15 0.1 0.25 0.3], 'FontSize', 14, ...
                            'FontWeight', 'bold', 'ForegroundColor', [0 1 1], 'BackgroundColor', [0.08 0.1 0.15]);

    % Knob pour le Duty Cycle
    uicontrol('Parent', ctrl_panel, 'Style', 'text', 'String', 'DUTY CYCLE (%)', ...
              'Units', 'normalized', 'Position', [0.5 0.1 0.1 0.3], 'BackgroundColor', [0.08 0.1 0.15], 'ForegroundColor', 'white');
    k_duty = uicontrol('Parent', ctrl_panel, 'Style', 'slider', 'Units', 'normalized', ...
                       'Position', [0.6 0.4 0.25 0.3], 'Min', 0, 'Max', 100, 'Value', 0);
    txt_duty_val = uicontrol('Parent', ctrl_panel, 'Style', 'text', 'String', '0.0 %', ...
                            'Units', 'normalized', 'Position', [0.6 0.1 0.25 0.3], 'FontSize', 14, ...
                            'FontWeight', 'bold', 'ForegroundColor', [1 0.8 0], 'BackgroundColor', [0.08 0.1 0.15]);

    % --- FONCTION DE ROTATION MOTEUR ---
    function rotate_propeller(val)
        speed_factor = (val/100) * 80; % VITESSE HYPER-SONIC
        angle_motor = angle_motor + speed_factor;
        R = [cosd(angle_motor) -sind(angle_motor); sind(angle_motor) cosd(angle_motor)];
        pts1 = R * [-0.8 0.8 0.04 -0.04; 0.04 0.04 -0.04 -0.04];
        pts2 = R * [0.04 0.04 -0.04 -0.04; -0.8 0.8 0.04 -0.04];
        set(hProp, 'XData', pts1(1,:), 'YData', pts1(2,:));
        set(hProp2, 'XData', pts2(1,:), 'YData', pts2(2,:));
    end

    % --- FONCTION DE GESTION DES LEDS ---
    function update_leds(val)
        % LED 1 (33%) - VERTE
        if val >= 33, set(leds_h(1), 'FaceColor', [0 1 0.2]); 
        else, set(leds_h(1), 'FaceColor', [0.1 0.1 0.1]); end
        % LED 2 (66%) - ORANGE
        if val >= 66, set(leds_h(2), 'FaceColor', [1 0.6 0]); 
        else, set(leds_h(2), 'FaceColor', [0.1 0.1 0.1]); end
        % LED 3 (95%) - ROUGE ALERTE
        if val >= 95, set(leds_h(3), 'FaceColor', [1 0 0]); 
        else, set(leds_h(3), 'FaceColor', [0.1 0.1 0.1]); end
    end

    % --- BOUCLE PRINCIPALE (REAL-TIME ENGINE) ---
    main_timer = timer('ExecutionMode', 'fixedRate', 'Period', 0.04, 'TimerFcn', @update_system);
    start(main_timer);
    set(fig, 'CloseRequestFcn', @(s,e) shutdown(main_timer, fig));

    function update_system(~, ~)
        if ~ishandle(fig), return; end
        
        % Récupération des données curseurettes
        current_f = get(k_freq, 'Value');
        current_d = get(k_duty, 'Value');
        
        % Mise à jour affichage texte
        set(txt_freq_val, 'String', [num2str(round(current_f)), ' Hz']);
        set(txt_duty_val, 'String', [num2str(current_d, '%.1f'), ' %']);
        
        % Mise à jour Signal PWM
        T_period = 1/current_f;
        pwm_signal = double(mod(t_scope, T_period) < (current_d/100)*T_period);
        set(hPlot, 'YData', pwm_signal);
        
        % Mise à jour Composants Visuels
        rotate_propeller(current_d);
        update_leds(current_d);
        
        % Effet de couleur dynamique sur le signal
        if current_d > 80
            set(hPlot, 'Color', [1 0.2 0.2]); % Rouge si charge haute
        else
            set(hPlot, 'Color', [0 1 0.5]);   % Vert normal
        end
        
        drawnow limitrate;
    end

    % --- FONCTION DE FERMETURE PROPRE ---
    function shutdown(t, f)
        try
            stop(t);
            delete(t);
            delete(f);
            disp('Système arrêté avec succès.');
        catch
            delete(f);
        end
    end
    % ---------------------------------------------------------------------
    % Documentation technique :
    % La MLI (Modulation de Largeur d'Impulsion) permet de contrôler la 
    % puissance fournie au moteur DC en faisant varier le rapport cyclique.
    % À l'ENIT, ce principe est fondamental pour l'électronique de puissance.
    % ---------------------------------------------------------------------
    % Fin du script.
end
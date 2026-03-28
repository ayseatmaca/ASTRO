clc;
clear;
close all;

%% Scenario Time (near newest TLE epoch)
startTime = datetime(2026,2,13,0,0,0);
stopTime  = startTime + days(3);
sampleTime = 60;

sc = satelliteScenario(startTime,stopTime,sampleTime);

%% File Paths
f1 = "C:/Users/Girinath_NU/Desktop/RC/tle_1hr.tle";
f2 = "C:/Users/Girinath_NU/Desktop/RC/tle_1day.tle";
f3 = "C:/Users/Girinath_NU/Desktop/RC/tle_3day.tle";
f4 = "C:/Users/Girinath_NU/Desktop/RC/tle_6day.tle";

%% Load satellites (all SGP4)
sat1 = satellite(sc,f1,"OrbitPropagator","sgp4"); % newest
sat2 = satellite(sc,f2,"OrbitPropagator","sgp4");
sat3 = satellite(sc,f3,"OrbitPropagator","sgp4");
sat4 = satellite(sc,f4,"OrbitPropagator","sgp4");

%% Color coding
sat1.Orbit.LineColor = "green";     % reference (fresh TLE)
sat2.Orbit.LineColor = "blue";      % 1 day old
sat3.Orbit.LineColor = "magenta";   % 3 day old
sat4.Orbit.LineColor = "red";       % 6 day old

sat1.MarkerColor = "green";
sat2.MarkerColor = "blue";
sat3.MarkerColor = "magenta";
sat4.MarkerColor = "red";

%% Viewer
v = satelliteScenarioViewer(sc);
campos(v,[2e7 2e7 2e7]);
play(sc);

%% Get states
[p1,~,time] = states(sat1);
[p2,~] = states(sat2);
[p3,~] = states(sat3);
[p4,~] = states(sat4);

%% Compute errors wrt latest TLE
err2 = vecnorm(p2 - p1,2,1)/1000;
err3 = vecnorm(p3 - p1,2,1)/1000;
err4 = vecnorm(p4 - p1,2,1)/1000;

%% Plot comparison
figure;
plot(time,err2,'b','LineWidth',1.5); hold on;
plot(time,err3,'m','LineWidth',1.5);
plot(time,err4,'r','LineWidth',1.5);

xlabel("Time");
ylabel("Position Error (km)");
title("TLE Ageing Error Comparison");
grid on;

legend("1 Day Old TLE","3 Day Old TLE","6 Day Old TLE", ...
       'Location','northeast');

fprintf("\nFinal Position Errors:\n");
fprintf("1 Day TLE error  : %.2f km\n", err2(end));
fprintf("3 Day TLE error  : %.2f km\n", err3(end));
fprintf("6 Day TLE error  : %.2f km\n", err4(end));


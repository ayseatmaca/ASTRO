clc;
clear;
close all;

%% -------------------------------------------------
%% Scenario
%% -------------------------------------------------
startTime = datetime(2026,2,13,0,0,0);
stopTime  = startTime + days(5);
sampleTime = 60;

sc = satelliteScenario(startTime,stopTime,sampleTime);

%% -------------------------------------------------
%% TLE Files
%% -------------------------------------------------
f1 = "C:/Users/Girinath_NU/Desktop/RC/tle_1hr.tle";
f2 = "C:/Users/Girinath_NU/Desktop/RC/tle_1day.tle";
f3 = "C:/Users/Girinath_NU/Desktop/RC/tle_3day.tle";
f4 = "C:/Users/Girinath_NU/Desktop/RC/tle_6day.tle";

%% -------------------------------------------------
%% Satellites (SGP4)
%% -------------------------------------------------
sat1 = satellite(sc,f1,"OrbitPropagator","sgp4"); % reference
sat2 = satellite(sc,f2,"OrbitPropagator","sgp4");
sat3 = satellite(sc,f3,"OrbitPropagator","sgp4");
sat4 = satellite(sc,f4,"OrbitPropagator","sgp4");

%% -------------------------------------------------
%% Ground Station
%% -------------------------------------------------
gs = groundStation(sc,"Latitude",10.778,"Longitude",79.137);
gs.MinElevationAngle = 10;

%% -------------------------------------------------
%% States
%% -------------------------------------------------
[p1,~,time] = states(sat1);
[p2,~] = states(sat2);
[p3,~] = states(sat3);
[p4,~] = states(sat4);

%% -------------------------------------------------
%% Position Error
%% -------------------------------------------------
posErr2 = vecnorm(p2-p1,2,1)/1000;
posErr3 = vecnorm(p3-p1,2,1)/1000;
posErr4 = vecnorm(p4-p1,2,1)/1000;

%% -------------------------------------------------
%% Antenna Pointing
%% -------------------------------------------------
[az1,el1,r1] = aer(gs,sat1);
[az2,el2,r2] = aer(gs,sat2);
[az3,el3,r3] = aer(gs,sat3);
[az4,el4,r4] = aer(gs,sat4);

azErr4 = abs(az4-az1);
elErr4 = abs(el4-el1);

%% -------------------------------------------------
%% SKY PLOT (Very intuitive)
%% -------------------------------------------------
figure;
polarplot(deg2rad(az1),90-el1,'g'); hold on;
polarplot(deg2rad(az4),90-el4,'r');
title("Sky Plot: True vs 6-Day Old TLE");
legend("Actual Satellite","Predicted (Old TLE)");

%% -------------------------------------------------
%% TRACKING LOST GRAPH
%% -------------------------------------------------
beamwidth = 5; % degrees typical antenna
trackingLost = azErr4 > beamwidth;

figure;
plot(time,trackingLost,'LineWidth',2);
ylim([0 1.2])
yticks([0 1])
yticklabels(["Tracking OK","Satellite Lost"])
title("Tracking Availability vs Time");
grid on;

%% -------------------------------------------------
%% DOPPLER ERROR
%% -------------------------------------------------
c=3e8; f0=437e6;

r1=r1(:); r4=r4(:);

rr1=[0;diff(r1)]/sampleTime;
rr4=[0;diff(r4)]/sampleTime;

dopErr4=abs((rr4-rr1)/c*f0);

figure;
plot(time,dopErr4,'r'); hold on;
yline(3000,'k--','Receiver Limit');
ylabel("Frequency Error (Hz)");
title("Receiver Doppler Tuning Failure");
legend("Prediction Error","Receiver Bandwidth");
grid on;

xlim([datetime(2026,2,13,"TimeZone","UTC")...
      datetime(2026,2,18,"TimeZone","UTC")])
ylim([0 9000])

%% -------------------------------------------------
%% ORBIT DRIFT VISUALIZATION
%% -------------------------------------------------
figure;
plot3(p1(1,:),p1(2,:),p1(3,:),'g'); hold on;
plot3(p4(1,:),p4(2,:),p4(3,:),'r');
axis equal; grid on;
title("Orbit Drift Due to Old TLE");
legend("True Orbit","Predicted Orbit");

%% -------------------------------------------------
%% PRINT NUMERICAL RESULTS
%% -------------------------------------------------
fprintf("\n===== FINAL RESULTS =====\n");

fprintf("\nMax Position Error (km)\n");
fprintf("1 day : %.2f\n3 day : %.2f\n6 day : %.2f\n",...
    max(posErr2),max(posErr3),max(posErr4));

fprintf("\nMax Pointing Error (deg)\n");
fprintf("Azimuth : %.2f\nElevation : %.2f\n",max(azErr4),max(elErr4));

fprintf("\nMax Doppler Error (Hz)\n");
fprintf("%.2f Hz\n",max(dopErr4));


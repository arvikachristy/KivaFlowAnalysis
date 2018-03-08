
% [arclen,az] = distance(-25.274398,133.775136,20.593684,78.96288);
% X = [-25.274398,133.775136;20.593684,78.96288];
% d = pdist(X,'euclidean');
% [res, reso]= lldistkm([-6.369028,34.888822],[-30.559482	22.937506]);
% 

function [d1km, d2km]=latlongReader(latlon1,latlon2)
radius=6371;
lat1=latlon1(1)*pi/180;
lat2=latlon2(1)*pi/180;
lon1=latlon1(2)*pi/180;
lon2=latlon2(2)*pi/180;
deltaLat=lat2-lat1;
deltaLon=lon2-lon1;
a=sin((deltaLat)/2)^2 + cos(lat1)*cos(lat2) * sin(deltaLon/2)^2;
c=2*atan2(sqrt(a),sqrt(1-a));
d1km=radius*c;    %Haversine distance

x=deltaLon*cos((lat1+lat2)/2);
y=deltaLat;
d2km=radius*sqrt(x*x + y*y); %Pythagoran distance

end
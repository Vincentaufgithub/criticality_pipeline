asdf2 = rebin(asdf2,4); % Rebin from 1 ms bins to 4 ms bins



% 
% x=gendata(10000,{"powerlaw",2.5});
% x=pldist(1000);
% asdf2=cbmodel(0.26);
% 
% % load sample_data.mat%Loadthedata
% Av=avprops(asdf2);%Findtheavalanches
% avgProfiles=avgshapes(Av.shape,Av.duration,"cutoffs",4,20);
% 
% [SNZsc,secondDrv,range,errors]= avshapecollapse(avgProfiles,"plot");
% 
% sigmaSNZsc=avshapecollapsestd(avgProfiles);

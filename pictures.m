
Pncc = spm_select(Inf,'nifti','Select noncentral chi maps');
N    = size(Pncc,1);
Pgau = spm_select(N, 'nifti','Select Gaussian maps');

Nncc = nifti(Pncc);
Ngau = nifti(Pgau);

disp(size(Nncc(1).dat))

sel   = {21:260,80:280,90};  % Example sagittal view
%sel   = {21:260,155,11:214};  % Example axial view
%sel   = {101:180,155,81:144}; % Example axial view - zoomed in

range = [0 0 0 0; 3 20000 3 50]; % Ranges work for mt, pd, r1, r2s
pic   = [];
dpic  = [];
for n=1:N
    % Read 2D slices
    ni   = squeeze(Nncc(n).dat(sel{:}));
    gi   = squeeze(Ngau(n).dat(sel{:}));

    % Transpose/flip etc if necessary
   %ni   = flipud(ni');
   %gi   = flipud(gi');

    % Rescale
    ni = max(min(ni,range(2,n)),range(1,n))/(range(2,n)-range(1,n));
    gi = max(min(gi,range(2,n)),range(1,n))/(range(2,n)-range(1,n));

    % Concatenate
    %pic   = [pic [ni; gi]]; % Top row is ni, bottom row is gi
    scale = 1; % You'll need to figure out the best scaling
    %dpic  = [dpic scale*(ni-gi)+0.5];
    dpic = scale*(ni-gi)+0.5;
    pic   = [pic [ni; gi; dpic]]; % Top row is ni, bottom row is gi
end

imagesc(pic)
axis image ij off
colormap(gray)

imwrite(pic,'gaus_gaus_sag.png');
%imwrite(dpic,'diff_chi_gaus_ax_zoom_dif.png');



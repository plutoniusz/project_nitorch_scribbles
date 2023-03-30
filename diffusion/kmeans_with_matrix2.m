  % Load Matrix2
x=load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/fdt_matrix2.dot');
M=full(spconvert(x));
% Calculate cross-correlation
CC  = 1+corrcoef(M');
% Do kmeans with k clusters
size(CC(~any(isnan(CC),2)));
k = 10;
idx = kmeans(CC,k);   % k is the number of clusters
% Load coordinate information to save results
addpath([getenv('FSLDIR') '/etc/matlab']);
[mask,~,scales] = read_avw('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/fdt_paths');
mask = 0*mask;
coord = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/coords_for_fdt_matrix2')+1;
ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));
[~,~,j] = unique(idx);
mask(ind) = j;
save_avw(mask,'/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/clusters_km','i',scales);
!fslcpgeom fdt_paths clusters
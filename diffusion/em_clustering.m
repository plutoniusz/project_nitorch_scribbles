% 
% X - 2d intensity histogram, dimenstions MxN,
%     where N is the number of voxels in seed region
%     and M is the number of target voxels
% P - matrix of means of multinominal distributions MxK
% g - mixing proportions of the clusters
% Z - latent variable matrix such that p(z_n|g) = \prod_{k=1}^K g_k^{z_{kn}}
% K - number of clusters
% N - number of seed voxels
% r - responsibilities kxn

main_path = '/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi';
x = load([main_path '/fsl_probtrackx-test_mask_transform_4/fdt_matrix2.dot']);
[phi,dim1,dim2] = spm_def2sparse('/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/modified/y_1_00001_sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0_mb.nii', '/data/underworld/home/kbas/03_data/derivatives/112111/20191115/dwi/qmap-preproc-b0/sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0.nii');
%[phi,dim1,dim2] = spm_def2sparse('/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/modified/y_1_00001_sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0_mb.nii', '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/modified/y_1_00001_sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0_mb.nii');

[a,b] = size(phi);
x = sparse(x(:,1), x(:,2), x(:,3), a, b);
pom = phi*x*phi';
%x = full(spconvert(x))';
[M,N] = size(x);
% arbitrary number of clusters
K = 8;
% initial p,r,g
p = 1+rand(M,K);
g = 1+rand(K,1);
g = g/sum(g);
r = ones(N,K);
l = ones(K,M);
h = ones(K,1);

[p,g,r] = em(x,p,g,1);
%[~, idx] = max(r, [], 2);
% % Load coordinate information to save results
% addpath([getenv('FSLDIR') '/etc/matlab']);
% [mask,~,scales] = read_avw('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/fdt_paths');
% mask = 0*mask;
% coord = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/coords_for_fdt_matrix2')+1;
% ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));
% [~,~,j] = unique(idx);
% mask(ind) = j;
% save_avw(mask,'/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/clusters_em','i',scales);


% Load coordinate information to save results
addpath([getenv('FSLDIR') '/etc/matlab']);
[mask,~,scales] = read_avw('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/fdt_paths');
mask = 0*mask;
coord = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/coords_for_fdt_matrix2')+1;
ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));

for i=1:K
    %[~, idx] = max(r, [], 2);
    %~,~,j] = unique(idx);
    mask(ind) = r(:, i);
    save_avw(mask,['/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/clusters_em_w' num2str(i)],'i',scales);
end


function [p,g,r,ll] = em(x,p,g,iter)
    for i= 1:iter
        [r,l,h] = e_step(x,p,g);
        [p,g] = m_step(x,r,K,g,p);
        ll_n = ll;
        ll = loglikelihood(x,p,g);
        if abs(ll-ll_n) < abs(ll*1e-9), break; end
    end
   
end

function ll = loglikelihood(x,p,g,r)
   ll = sum(LSE(log(p)'*X + log(g),1)); 
end


function [r,l,h] = e_step(x,p,g)
% returns the responsibilities of latent variables
    [M,N] = size(x);
    ppom = p;
    ppom(ppom<1e-320) = 1e-320;
    size(ppom);
    l = log(ppom)'; % KxM
    h = log(g); % 1xK
    tom = zeros(8, 1);
    for n = 1:N
        tom = l*x(:,n);
        r(n,:) = softmax(tom +h);
    end
end


function [p, g] = m_step(x,r,K,g,p)
    [M,N] = size(x);
    for k = 1:K
        %p(:,k) = sum(x*r(:,k), 2)./sum(r(:,k), 1);
        pom = zeros(M,N);
        for n = 1:N
            pom(:,n) = x(:,n)*r(n,k);
        end
        p(:,k) = sum(pom, 2)/sum(r(:,k), 1); %mxk
    end
    g = sum(r,1)/N;
end

function sig = softmax(a)
    t = max(a,[],1);
%     o = vpa(exp(sym(a-t)));
    o = exp(a-t);
    sig = o/sum(o);
end
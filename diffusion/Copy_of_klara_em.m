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

if true
%     x = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl-probtrackx-1/fdt_matrix2.dot');
%     X = full(spconvert(x))';
%     K = 10;

    main_path = '/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi';
    x = load([main_path '/fsl_probtrackx-test_mask_transform_7/fdt_matrix2.dot']);
    %[phi,dim1,dim2] = spm_def2sparse('/data/underworld/kbas/03_data/source/mri/112111/20191115/10/modified/y_y_1_00001_sMP02874-0010-00001-000224-01_mb_res.nii', '/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/qmap-preproc-b0/sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0.nii');
    %x = spconvert(x);

    %[a,b] = size(phi);
    %X = sparse(x(:,1), x(:,2), x(:,3), a, b);
    %image = full(spconvert(x));
    %image = image(1:691, 1:1000);
    %X = phi*X*phi';
    %save_avw(X, ['/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/x_phi'] ,'i',scales);
    X = full(spconvert(x))';
    K = 10;

%     main_path = '/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi';
%     x = load([main_path '/fsl_probtrackx-test_mask_transform_4/fdt_matrix2.dot']);
%     [phi,dim1,dim2] = spm_def2sparse('/data/underworld/kbas/03_data/source/mri/112111/20191115/10/modified/y_y_1_00001_sMP02874-0010-00001-000224-01_mb_res.nii', '/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/qmap-preproc-b0/sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0.nii');
%     %x = spconvert(x);
% 
%     [a,b] = size(phi);
%     X = sparse(x(:,1), x(:,2), x(:,3), a, b);
%     X = phi*X*phi';
%     save_avw(X, ['/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/x_phi'] ,'i',scales);
else
    K  = 10;
    N  = 1000;
    M  = 20;
    g0 = softmax(randn(K,1)*0.5);
    P0 = softmax(randn(M,K),1);
    R0 = multinom_random(repmat(g0,[1 N]),1);
    X  = multinom_random(P0*R0,1000);
end
[M,N] = size(X);
P     = exp(randn(M,K)*0.01);
P     = P./sum(P,1);
g     = ones(K,1)/K;

[P,g,R,ll] = em(X,P,g,1000);
% % Load coordinate information to save results
% addpath([getenv('FSLDIR') '/etc/matlab']);
% [mask,~,scales] = read_avw('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/fdt_paths');
% mask = 0*mask;
% coord = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/coords_for_fdt_matrix2')+1;
% ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));
% [~,~,j] = unique(idx);
% mask(ind) = j;
% save_avw(mask,'/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/clusters_1','i',scales);

% Load coordinate information to save results
addpath([getenv('FSLDIR') '/etc/matlab']);
[mask,~,scales] = read_avw('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_7/fdt_paths.nii.gz');
mask = 0*mask;
coord = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_7/coords_for_fdt_matrix2')+1;
ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));

for i=1:K
    %[~, idx] = max(r, [], 2);
    %~,~,j] = unique(idx);
    mask(ind) = R(i, :);
    save_avw(mask, ['/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_7/clusters_em' num2str(i)] ,'i',scales);
end

function Z = multinom_random(P,Nsamp)
    if nargin<2
        N = 1;
    end
    [M,N] = size(P);
    U     = cumsum(P,1); %cumulative column sum                 % Upper value
    L     = [zeros(1,N); U(1:(end-1),:)]; % Lower values
    Z     = zeros(M,N);
    for i=1:Nsamp
        t = rand(1,N);
        s = sum((t>=L & t<U).*(1:M)',1);
        Z = Z + full(sparse(s,1:N,1,M,N));
    end
end


function [P,g,R,ll] = em(X,P,g,nit)
    ll = -Inf;
    for iter= 1:nit
        R     = e_step(X,P,g);
        [P,g] = m_step(X,R);
        ll_o  = ll;
        ll    = loglikelihood(X,P,g);
        disp(ll)
        if abs(ll-ll_o) < abs(ll*1e-9); break; end
    end
    %ll = ll + factorial_stuff(X);
end


function ll = loglikelihood(X,P,g,R)
    ll = sum(LSE(log(P)'*X + log(g),1));
end


function R = e_step(X,P,g)
    R = softmax(log(P)'*X + log(g),1);
end


function [P, g] = m_step(X,R)
    alpha0 = 1e-3; % Behaves like having a Dirichlet prior
    P = X*R' + alpha0;
    P = P./sum(P,1);
    g = sum(R,2) + 1e-10; % To prevent numerical problems
    g = g/sum(g);
end


function S = softmax(A,dim)
    % exp(A)./sum(exp(A),dim)
    if nargin<2
        dim = 1;
    end
    t = max(A,[],dim);
    T = exp(A - t);
    S = T./sum(T,dim);
end

function L = LSE(A,dim)
    % log(sum(exp(A)),dim)
    % https://en.wikipedia.org/wiki/LogSumExp
    if nargin<2
        dim = 1;
    end
    t = max(A,[],dim);
    L = log(sum(exp(A - t))) + t;
end


function ll_const = factorial_stuff(X)
    ll_const = sum(logfactorial(sum(X,1)) - sum(logfactorial(X),1));
end


function L = logfactorial(X)
    % log(X!)
    L = gammaln(X+1);
end



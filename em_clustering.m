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

x = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/fdt_matrix2.dot');
x = full(spconvert(x))';
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

[p,g,r] = em(x,p,g,K);
% % Load coordinate information to save results
% addpath([getenv('FSLDIR') '/etc/matlab']);
% [mask,~,scales] = read_avw('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/fdt_paths');
% mask = 0*mask;
% coord = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/coords_for_fdt_matrix2')+1;
% ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));
% [~,~,j] = unique(idx);
% mask(ind) = j;
% save_avw(mask,'/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl_probtrackx-test_mask_transform_4/clusters_1','i',scales);



function [p,g,r] = em(x,p,g,K)
    for i= 1:30
        [r,l,h] = e_step(x,p,g);
        [p,g] = m_step(x,r,K,g,p);
    end
end


function [r,l,h] = e_step(x,p,g)
% returns the responsibilities of latent variables
    [M,N] = size(x);
    l = log(p+10e-50)'; % KxM
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

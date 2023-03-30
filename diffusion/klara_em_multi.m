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
    K = 10;

    path_list = [ "/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/128221/20190920/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/130519/20191115/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/170192/20190111/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/176117/20190222/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/208010/20200110/dwi/fsl-probtrackx-2/fdt_matrix2.dot"; 
        "/data/underworld/kbas/03_data/derivatives/210022/20190621/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/211787/20191011/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/214685/20201204/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/232237/20191018/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/308597/20191129/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/324038/20191213/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/330406/20191122/dwi/fsl-probtrackx-2/fdt_matrix2.dot";
        "/data/underworld/kbas/03_data/derivatives/346878/20190531/dwi/fsl-probtrackx-2/fdt_matrix2.dot"];

%     def_list = ["/data/underworld/kbas/03_data/processed/y_1_00001_sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00002_sub-128221_ses-20190920_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00003_sub-130519_ses-20191115_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00004_sub-170192_ses-20190111_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00005_sub-176117_ses-20190222_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00006_sub-208010_ses-20200110_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00007_sub-210022_ses-20190621_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00008_sub-211787_ses-20191011_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00009_sub-214685_ses-20201204_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00010_sub-232237_ses-20191018_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00011_sub-308597_ses-20191129_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00012_sub-324038_ses-20191213_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00013_sub-330406_ses-20191122_space-orig_desc-dwi-skullstripped_b0_mb.nii";
%         "/data/underworld/kbas/03_data/processed/y_1_00014_sub-346878_ses-20190531_space-orig_desc-dwi-skullstripped_b0_mb.nii"];

    def_list = ["/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation112111.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation128221.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation130519.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation170192.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation176117.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation208010.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation210022.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation211787.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation214685.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation232237.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation308597.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation324038.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation330406.nii";
        "/data/underworld/kbas/03_data/processed/test_mb/y_resliced_deformation346878.nii"];

    b0_list = ["/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/qmap-preproc-b0/sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/128221/20190920/dwi/qmap-preproc-b0/sub-128221_ses-20190920_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/130519/20191115/dwi/qmap-preproc-b0/sub-130519_ses-20191115_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/170192/20190111/dwi/qmap-preproc-b0/sub-170192_ses-20190111_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/176117/20190222/dwi/qmap-preproc-b0/sub-176117_ses-20190222_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/208010/20200110/dwi/qmap-preproc-b0/sub-208010_ses-20200110_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/210022/20190621/dwi/qmap-preproc-b0/sub-210022_ses-20190621_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/211787/20191011/dwi/qmap-preproc-b0/sub-211787_ses-20191011_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/214685/20201204/dwi/qmap-preproc-b0/sub-214685_ses-20201204_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/232237/20191018/dwi/qmap-preproc-b0/sub-232237_ses-20191018_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/308597/20191129/dwi/qmap-preproc-b0/sub-308597_ses-20191129_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/324038/20191213/dwi/qmap-preproc-b0/sub-324038_ses-20191213_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/330406/20191122/dwi/qmap-preproc-b0/sub-330406_ses-20191122_space-orig_desc-dwi-skullstripped_b0.nii";
        "/data/underworld/kbas/03_data/derivatives/346878/20190531/dwi/qmap-preproc-b0/sub-346878_ses-20190531_space-orig_desc-dwi-skullstripped_b0.nii"];

        gen_list = [ "/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/128221/20190920/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/130519/20191115/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/170192/20190111/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/176117/20190222/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/208010/20200110/dwi/fsl-probtrackx-2"; 
        "/data/underworld/kbas/03_data/derivatives/210022/20190621/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/211787/20191011/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/214685/20201204/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/232237/20191018/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/308597/20191129/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/324038/20191213/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/330406/20191122/dwi/fsl-probtrackx-2";
        "/data/underworld/kbas/03_data/derivatives/346878/20190531/dwi/fsl-probtrackx-2"];

    x_list = cell(14,1);
    whole_list = cell(14,1);
    phi_list = cell(14,1);
    addpath([getenv('FSLDIR') '/etc/matlab']);
%     [mask,~,scales] = read_avw('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl-probtrackx-2/fdt_paths.nii.gz');
%     mask = 0*mask;
%     coord = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl-probtrackx-2/coords_for_fdt_matrix2')+1;
%     ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));
% 
%     coord_wb = load('/data/underworld/kbas/03_data/derivatives/112111/20191115/dwi/fsl-probtrackx-2/tract_space_coords_for_fdt_matrix2')+1;
%     ind_wb = sub2ind(size(mask), coord_wb(:,1), coord_wb(:,2), coord_wb(:,3));
    
    minimum_m = 1713600;
    minimum_n = 1713600;
    maximum_m = 1;
    maximum_n = 1;
    figure;
    for i=1:14
        x = spconvert(load(path_list(i)));
        [phi_list{i},dim1,dim2] = spm_def2sparse(num2str(def_list(i)), num2str(b0_list(i)));
        [a1,a2] = size(phi_list{i});

        [mask,~,scales] = read_avw([gen_list{i} '/fdt_paths.nii.gz']);
        mask = 0*mask;
        coord = load([gen_list{i} '/coords_for_fdt_matrix2'])+1;
        ind   = sub2ind(size(mask),coord(:,1),coord(:,2),coord(:,3));
        coord_wb = load([gen_list{i} '/tract_space_coords_for_fdt_matrix2'])+1;
        ind_wb = sub2ind(size(mask), coord_wb(:,1), coord_wb(:,2), coord_wb(:,3));

        empty = sparse(a1, a1);
        empty(ind, ind_wb) = x;
        whole_list{i} = phi_list{i}'*empty*phi_list{i};

        spy(whole_list{i});
        hold on;
        
        [a,b] = find(whole_list{i});
        minimum_m = min(min(a), minimum_m);
        maximum_m = max(max(a), maximum_m);
        minimum_n = min(min(b), minimum_n);
        maximum_n = max(max(b), maximum_n);
        
    end
    hold off
    figure;
    for i=1:14
        x_list{i} = whole_list{i}(minimum_m:maximum_m, minimum_n:maximum_n);
        spy(x_list{i});
        hold on;
    end
    hold off
   

else
    K  = 10;
    N  = 1000;
    M  = 20;
    g0 = softmax(randn(K,1)*0.5);
    P0 = softmax(randn(M,K),1);
    R0 = multinom_random(repmat(g0,[1 N]),1);
    X  = multinom_random(P0*R0,1000);
end

X=x_list{1}';
[M,N] = size(X);
P     = exp(randn(M,K)*0.01);
P     = P./sum(P,1);
g     = ones(K,1)/K;

[P,g,R,ll] = em(X,P,g,1000);

for i=1:K
    mask(ind) = full(R(i, :));
    save_avw(mask, [gen_list '/clusters_test_' num2str(i)] ,'i',scales);
end




function Z = multinom_random(P,Nsamp)
    if nargin<2
        N = 1;
    end
    [M,N] = size(P);
    U     = cumsum(P,1); %cumulative column sum  % Upper value
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
        ll    = loglikelihood(X,P,g,R);
        if abs(ll-ll_o) < abs(ll*1e-9); break; end
    end
    %ll = ll + factorial_stuff(X);
end


function ll = loglikelihood(X,P,g,R)
    ll = sum(LSE(log(P)'*X + log(g),1));
end


function R = e_step(X,P,g)
    R = sparse(softmax(log(P)'*X + log(g),1));
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


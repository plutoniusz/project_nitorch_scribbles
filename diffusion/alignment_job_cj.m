%-----------------------------------------------------------------------
% Job saved on 13-Dec-2021 16:32:42 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (12.6)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
cwd = pwd;

% Align all the T1w data to the first PDw scan
matlabbatch{1}.spm.spatial.coreg.estimate.ref   = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000224-01.nii,1']};
matlabbatch{1}.spm.spatial.coreg.estimate.source= {['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000224-01.nii,1']};
matlabbatch{1}.spm.spatial.coreg.estimate.other = {
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000448-02.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000672-03.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000896-04.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001120-05.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001344-06.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001568-07.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001792-08.nii,1']
                                                   ['/data/underworld/kbas/03_data/raw/112111/20191115/anat/Results/Supplementary/sensMap_HC_over_BC_division_T1.nii,1']
                                                   };
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

% Align all the MTw data to the first PDw scan
matlabbatch{2}.spm.spatial.coreg.estimate.ref   = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000224-01.nii,1']};
matlabbatch{2}.spm.spatial.coreg.estimate.source= {['/data/underworld/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000224-01.nii,1']};
matlabbatch{2}.spm.spatial.coreg.estimate.other = {
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000448-02.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000672-03.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000896-04.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-001120-05.nii,1']
                                                   ['/data/underworld/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-001344-06.nii,1']
                                                   ['/data/underworld/kbas/03_data/raw/112111/20191115/anat/Results/Supplementary/sensMap_HC_over_BC_division_MT.nii,1']
                                                   };
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

% Align the B1 data to the first PDw scan
matlabbatch{3}.spm.spatial.coreg.estimate.ref   = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000224-01.nii,1']};
matlabbatch{3}.spm.spatial.coreg.estimate.source= {['/data/underworld/kbas/03_data/raw/112111/20191115/anat/Results/Supplementary/sMP02874-0005-00001-000001-01_B1ref.nii,1']};
matlabbatch{3}.spm.spatial.coreg.estimate.other = {['/data/underworld/kbas/03_data/raw/112111/20191115/anat/Results/Supplementary/sMP02874-0005-00001-000001-01_B1map.nii,1']};
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];


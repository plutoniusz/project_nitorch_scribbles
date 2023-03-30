%-----------------------------------------------------------------------
% Job saved on 13-Dec-2021 16:32:42 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (12.6)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
cwd = pwd;

% Align all the T1w data to the first PDw scan
matlabbatch{1}.spm.spatial.coreg.estimate.ref   = {[cwd '/MPM/pdw_mfc_3dflash_v1i_R4_0009/anon_s2018-02-28_18-26-185345-00001-00224-1.nii,1']};
matlabbatch{1}.spm.spatial.coreg.estimate.source= {[cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-00224-1.nii,1']};
matlabbatch{1}.spm.spatial.coreg.estimate.other = {
                                                   [cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-00448-2.nii,1']
                                                   [cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-00672-3.nii,1']
                                                   [cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-00896-4.nii,1']
                                                   [cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-01120-5.nii,1']
                                                   [cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-01344-6.nii,1']
                                                   [cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-01568-7.nii,1']
                                                   [cwd '/MPM/t1w_mfc_3dflash_v1i_R4_0015/anon_s2018-02-28_18-26-190921-00001-01792-8.nii,1']
                                                   [cwd '/MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_T1.nii,1']
                                                   };
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

% Align all the MTw data to the first PDw scan
matlabbatch{2}.spm.spatial.coreg.estimate.ref   = {[cwd '/MPM/pdw_mfc_3dflash_v1i_R4_0009/anon_s2018-02-28_18-26-185345-00001-00224-1.nii,1']};
matlabbatch{2}.spm.spatial.coreg.estimate.source= {[cwd '/MPM/mtw_mfc_3dflash_v1i_R4_0012/anon_s2018-02-28_18-26-190132-00001-00224-1.nii,1']};
matlabbatch{2}.spm.spatial.coreg.estimate.other = {
                                                   [cwd '/MPM/mtw_mfc_3dflash_v1i_R4_0012/anon_s2018-02-28_18-26-190132-00001-00448-2.nii,1']
                                                   [cwd '/MPM/mtw_mfc_3dflash_v1i_R4_0012/anon_s2018-02-28_18-26-190132-00001-00672-3.nii,1']
                                                   [cwd '/MPM/mtw_mfc_3dflash_v1i_R4_0012/anon_s2018-02-28_18-26-190132-00001-00896-4.nii,1']
                                                   [cwd '/MPM/mtw_mfc_3dflash_v1i_R4_0012/anon_s2018-02-28_18-26-190132-00001-01120-5.nii,1']
                                                   [cwd '/MPM/mtw_mfc_3dflash_v1i_R4_0012/anon_s2018-02-28_18-26-190132-00001-01344-6.nii,1']
                                                   [cwd '/MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_MT.nii,1']
                                                   };
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{2}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

% Align the B1 data to the first PDw scan
matlabbatch{3}.spm.spatial.coreg.estimate.ref   = {[cwd '/MPM/pdw_mfc_3dflash_v1i_R4_0009/anon_s2018-02-28_18-26-185345-00001-00224-1.nii,1']};
matlabbatch{3}.spm.spatial.coreg.estimate.source= {[cwd '/MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/anon_s2018-02-28_18-26-184837-00001-00001-1_B1ref.nii,1']};
matlabbatch{3}.spm.spatial.coreg.estimate.other = {[cwd '/MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/anon_s2018-02-28_18-26-184837-00001-00001-1_B1map.nii,1']};
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{3}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];


%-----------------------------------------------------------------------
% Job saved on 14-Mar-2023 17:05:04 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.dir = '<UNDEFINED>';
matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.filter = 'sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii';
matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPListRec';
matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.dir = '<UNDEFINED>';
matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.filter = 'sMP\d{5}-\d{4}-\d{5}-\d{6}-\d{2}\.nii';
matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.rec = '<UNDEFINED>';
matlabbatch{3}.spm.spatial.coreg.estwrite.ref(1) = cfg_dep('File Selector (Batch Mode): Selected Files (sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
matlabbatch{3}.spm.spatial.coreg.estwrite.source(1) = cfg_dep('File Selector (Batch Mode): Selected Files (sMP\d{5}-\d{4}-\d{5}-\d{6}-\d{2}\.nii)', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
matlabbatch{3}.spm.spatial.coreg.estwrite.other = {''};
matlabbatch{3}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
matlabbatch{3}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
matlabbatch{3}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{3}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
matlabbatch{3}.spm.spatial.coreg.estwrite.roptions.interp = 4;
matlabbatch{3}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
matlabbatch{3}.spm.spatial.coreg.estwrite.roptions.mask = 0;
matlabbatch{3}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';

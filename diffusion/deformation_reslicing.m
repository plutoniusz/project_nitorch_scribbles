
subjects = [112111 128221 130519 170192 176117 208010 210022 211787 214685 232237 308597 324038 330406 346878];
for subject=subjects

    subject = num2str(subject);

    spm('defaults','fmri');
    spm_jobman('initcfg');


    matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.dir = {['/data/underworld/kbas/03_data/derivatives/' subject]};
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.filter = '^sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii$';
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPListRec';

    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.dir = {'/data/underworld/kbas/03_data/processed/test_mb'};
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.filter = ['y_1_\d{5}_sub-' subject '_ses-\d{1,8}_space-orig_desc-dwi-skullstripped_b0_mb\.nii'];
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPList';

    %matlabbatch{3}.spm.util.defs.comp{1}.id.space(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii$)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    %matlabbatch{3}.spm.util.defs.comp{2}.def(1) = cfg_dep(['File Selector (Batch Mode): Selected Files (y_1_\d{5}_sub-' subject '_ses-\d{1,8}_space-orig_desc-dwi-skullstripped_b0_mb\.nii)'], substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    
    matlabbatch{3}.spm.util.defs.comp{1}.idbbvox.vox = [1.7143 1.7143 1.7100];
    matlabbatch{3}.spm.util.defs.comp{1}.idbbvox.bb = [NaN NaN NaN
                                                      NaN NaN NaN];
    matlabbatch{3}.spm.util.defs.out = {};
    matlabbatch{3}.spm.util.defs.comp{2}.def(1) = cfg_dep(['File Selector (Batch Mode): Selected Files (y_1_\d{5}_sub-' subject '_ses-\d{1,8}_space-orig_desc-dwi-skullstripped_b0_mb\.nii)'], substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));

    matlabbatch{3}.spm.util.defs.out{1}.savedef.ofname = ['resliced_deformation_' subject];
    matlabbatch{3}.spm.util.defs.out{1}.savedef.savedir.saveusr = {'/data/underworld/kbas/03_data/processed/test_mb'};
    matlabbatch{3}.spm.util.defs.out{2}.push.fnames(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii$)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{3}.spm.util.defs.out{2}.push.weight = {''};
    matlabbatch{3}.spm.util.defs.out{2}.push.savedir.saveusr = {'/data/underworld/kbas/03_data/processed/test_mb'};
    matlabbatch{3}.spm.util.defs.out{2}.push.fov.file(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii$)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{3}.spm.util.defs.out{2}.push.preserve = 0;
    matlabbatch{3}.spm.util.defs.out{2}.push.fwhm = [0 0 0];
    matlabbatch{3}.spm.util.defs.out{2}.push.prefix = 'average_space';

    spm_jobman('run',matlabbatch);
end
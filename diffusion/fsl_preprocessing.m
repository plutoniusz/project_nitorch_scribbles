%-----------------------------------------------------------------------
% Job saved on 15-Mar-2023 23:37:46 by cfg_util (rev $Rev: 8183 $)
% spm SPM - SPM12 (12.6)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
% 116284  115326 133749 242234  260478 307789
% 
subjects = [112111 128221 130519 170192 176117 208010 210022 211787 214685 232237 308597 324038 330406 346878]; % Replace with a list of all of the subjects you wish to analyze
for subject=subjects

    subject = num2str(subject);

    spm('defaults','fmri');
    spm_jobman('initcfg');

    matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.dir = {['/data/underworld/kbas/03_data/derivatives/' subject]};
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.filter = '^sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii$';
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPListRec';
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.dir = {['/data/underworld/kbas/03_data/source/mri/' subject]};
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.filter = '^sMP\d{5}-0010-\d{5}-\d{6}-01\.nii';
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPListRec';
    matlabbatch{3}.spm.tools.mb.fil.images(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sMP\d{5}-0010-\d{5}-\d{6}-01\.nii)', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{4}.spm.spatial.coreg.estimate.ref(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii$)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{4}.spm.spatial.coreg.estimate.source(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sMP\d{5}-0010-\d{5}-\d{6}-01\.nii)', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{4}.spm.spatial.coreg.estimate.other(1) = cfg_dep('Image Labelling: Labelled brains', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','labels', '()',{':'}));
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
    matlabbatch{5}.cfg_basicio.file_dir.file_ops.cfg_file_split.name = 'estimates';
    matlabbatch{5}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('Coregister: Estimate: Coregistered Images', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
    matlabbatch{5}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {2};
    matlabbatch{6}.spm.spatial.coreg.write.ref(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sub-\d+_ses-\d+_space-orig_desc-dwi-skullstripped_b0\.nii$)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{6}.spm.spatial.coreg.write.source(1) = cfg_dep('File Set Split: File set (1)', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{6}.spm.spatial.coreg.write.roptions.interp = -1;
    matlabbatch{6}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
    matlabbatch{6}.spm.spatial.coreg.write.roptions.mask = 0;
    matlabbatch{6}.spm.spatial.coreg.write.roptions.prefix = 'r';
    matlabbatch{7}.spm.util.imcalc.input(1) = cfg_dep('Coregister: Reslice: Resliced Images', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rfiles'));
    matlabbatch{7}.spm.util.imcalc.output = 'thalamus_mask_diff';
    matlabbatch{7}.spm.util.imcalc.outdir = {['/data/underworld/home/kbas/03_data/processed_dif/' subject]};
    matlabbatch{7}.spm.util.imcalc.expression = '(i1==59) + (i1==60)';
    matlabbatch{7}.spm.util.imcalc.var = struct('name', {}, 'value', {});
    matlabbatch{7}.spm.util.imcalc.options.dmtx = 0;
    matlabbatch{7}.spm.util.imcalc.options.mask = 0;
    matlabbatch{7}.spm.util.imcalc.options.interp = 1;
    matlabbatch{7}.spm.util.imcalc.options.dtype = 4;
    matlabbatch{8}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.files(1) = cfg_dep('Image Calculator: ImCalc Computed Image: thalamus_mask_diff', substruct('.','val', '{}',{7}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{8}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.outdir = {''};
    matlabbatch{8}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.keep = true;
    matlabbatch{9}.spm.util.imcalc.input(1) = cfg_dep('Coregister: Reslice: Resliced Images', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rfiles'));
    matlabbatch{9}.spm.util.imcalc.output = 'amygdala_mask_diff';
    matlabbatch{9}.spm.util.imcalc.outdir = {['/data/underworld/home/kbas/03_data/processed_dif/' subject]};
    matlabbatch{9}.spm.util.imcalc.expression = '(i1==31) + (i1==32)';
    matlabbatch{9}.spm.util.imcalc.var = struct('name', {}, 'value', {});
    matlabbatch{9}.spm.util.imcalc.options.dmtx = 0;
    matlabbatch{9}.spm.util.imcalc.options.mask = 0;
    matlabbatch{9}.spm.util.imcalc.options.interp = 1;
    matlabbatch{9}.spm.util.imcalc.options.dtype = 4;
    matlabbatch{10}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.files(1) = cfg_dep('Image Calculator: ImCalc Computed Image: amygdala_mask_diff', substruct('.','val', '{}',{9}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{10}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.outdir = {''};
    matlabbatch{10}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.keep = true;
    spm_jobman('run',matlabbatch);
end
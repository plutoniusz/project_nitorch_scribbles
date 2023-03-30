%-----------------------------------------------------------------------
% Job saved on 26-Oct-2022 23:55:26 by cfg_util (rev $Rev: 8183 $)
% spm SPM - SPM12 (12.6)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'diff_space';
matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{'/data/underworld/home/kbas/03_data/derivatives/112111/20191115/dwi/qmap-preproc-b0/sub-112111_ses-20191115_space-orig_desc-dwi-skullstripped_b0.nii'}};
matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'quantitative_space';
%%
matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {
                                                                     {
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000224-01.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000448-02.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000672-03.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000896-04.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001120-05.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001344-06.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001568-07.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-001792-08.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000224-01.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000448-02.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000672-03.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000896-04.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-001120-05.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-001344-06.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-001568-07.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-001792-08.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000224-01.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000448-02.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000672-03.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000896-04.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-001120-05.nii'
                                                                     '/data/underworld/home/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-001344-06.nii'
                                                                     }
                                                                     }';
%%
matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.name = 'quantitative_space_split';
matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('Named File Selector: quantitative_space(1) - Files', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {
                                                                     1
                                                                     [2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22]
                                                                     }';
matlabbatch{4}.spm.spatial.coreg.estimate.ref(1) = cfg_dep('Named File Selector: diff_space(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
matlabbatch{4}.spm.spatial.coreg.estimate.source(1) = cfg_dep('File Set Split: quantitative_space_split (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
matlabbatch{4}.spm.spatial.coreg.estimate.other(1) = cfg_dep('File Set Split: quantitative_space_split (2)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{2}));
matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
matlabbatch{5}.cfg_basicio.run_ops.runjobs.jobs = {'/data/underworld/home/kbas/project_nitorch_scribbles/spm_label.m'};
matlabbatch{5}.cfg_basicio.run_ops.runjobs.inputs = {cell(1, 0)};
matlabbatch{5}.cfg_basicio.run_ops.runjobs.save.dontsave = false;
matlabbatch{5}.cfg_basicio.run_ops.runjobs.missing = 'skip';
matlabbatch{6}.cfg_basicio.file_dir.file_ops.file_fplist.dir = {'/data/underworld/home/kbas/03_data/derivatives/112111/20191115/dwi'};
matlabbatch{6}.cfg_basicio.file_dir.file_ops.file_fplist.filter = '^label\w*';
matlabbatch{6}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPList';
matlabbatch{7}.spm.spatial.coreg.write.ref(1) = cfg_dep('Named File Selector: diff_space(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
matlabbatch{7}.spm.spatial.coreg.write.source(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^label\w*)', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
matlabbatch{7}.spm.spatial.coreg.write.roptions.interp = -1;
matlabbatch{7}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
matlabbatch{7}.spm.spatial.coreg.write.roptions.mask = 0;
matlabbatch{7}.spm.spatial.coreg.write.roptions.prefix = 'r';

%-----------------------------------------------------------------------
% Job saved on 10-Mar-2023 21:13:55 by cfg_util (rev $Rev: 8183 $)
% spm SPM - SPM12 (12.6)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
% file registration and image calculation for the comparison of chi and gauss noise modelling 

subjects = [115326 116284 128221 130519 133749 170192 176117 208010 210022 211787 214685 232237 242234 260478 308597 324038 330406 346878]; % Replace with a list of all of the subjects you wish to analyze

for subject=subjects

    subject = num2str(subject);

    spm('defaults','fmri');
    spm_jobman('initcfg');

    
    matlabbatch{1}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.name = 'subject_folder';
    matlabbatch{1}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.dirs = {{['/data/underworld/home/kbas/03_data/source_qmri_pd_2/mri/' subject]}};
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.dir(1) = cfg_dep('Named Directory Selector: subject_folder(1)', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.filter = '^sMP.*-(0010|0013|0016)-.*\.nii';
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPListRec';
    matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.name = 'echos';
%     matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sMP.*-(0010|0013|0016)-.*\.nii)', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
%     matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {
%                                                                          1
%                                                                          2
%                                                                          [3 4 5 6 7 8]
%                                                                          9
%                                                                          [10 11 12 13 14 15 16]
%                                                                          17
%                                                                          [18 19 20 21 22]
%                                                                          };
    matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^sMP.*-(0010|0013|0016)-.*\.nii)', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {
                                                                         9
                                                                         10
                                                                         [11 12 13 14 15 16]
                                                                         1
                                                                         [2 3 4 5 6 7 8]
                                                                         17
                                                                         [18 19 20 21 22]
                                                                         };
    matlabbatch{4}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.name = 'field_maps';
    matlabbatch{4}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.dirs = {{['/data/underworld/home/kbas/03_data/raw_qmri_pd_2/' subject]}};
    matlabbatch{5}.cfg_basicio.file_dir.file_ops.file_fplist.dir(1) = cfg_dep('Named Directory Selector: field_maps(1)', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
    matlabbatch{5}.cfg_basicio.file_dir.file_ops.file_fplist.filter = '^(sMP\d{5}-\d{4}-\d{5}-\d{6}-\d{2}(map|ref).nii|sensMap.*_(MT|PD|T1).nii|sMP\d{5}-\d{4}-\d{5}-\d{6}-\d{2}_B1(ref|map).nii)$';
    matlabbatch{5}.cfg_basicio.file_dir.file_ops.file_fplist.rec = 'FPListRec';
    matlabbatch{6}.cfg_basicio.file_dir.file_ops.cfg_file_split.name = 'field_maps';
    matlabbatch{6}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('File Selector (Batch Mode): Selected Files (^(sMP\d{5}-\d{4}-\d{5}-\d{6}-\d{2}(map|ref).nii|sensMap.*_(MT|PD|T1).nii|sMP\d{5}-\d{4}-\d{5}-\d{6}-\d{2}_B1(ref|map).nii)$)', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{6}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {
                                                                         3%3
                                                                         5%4
                                                                         4%5
                                                                         };
    matlabbatch{7}.spm.spatial.coreg.estimate.ref(1) = cfg_dep('File Set Split: echos (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{7}.spm.spatial.coreg.estimate.source(1) = cfg_dep('File Set Split: echos (2)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{2}));
    matlabbatch{7}.spm.spatial.coreg.estimate.other(1) = cfg_dep('File Set Split: echos (3)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{3}));
    matlabbatch{7}.spm.spatial.coreg.estimate.other(2) = cfg_dep('File Set Split: field_maps (3)', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{3}));
    matlabbatch{7}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
    matlabbatch{7}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
    matlabbatch{7}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{7}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
    matlabbatch{8}.spm.spatial.coreg.estimate.ref(1) = cfg_dep('File Set Split: echos (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{8}.spm.spatial.coreg.estimate.source(1) = cfg_dep('File Set Split: echos (4)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{4}));
    matlabbatch{8}.spm.spatial.coreg.estimate.other(1) = cfg_dep('File Set Split: echos (5)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{5}));
    matlabbatch{8}.spm.spatial.coreg.estimate.other(2) = cfg_dep('File Set Split: field_maps (2)', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{2}));
    matlabbatch{8}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
    matlabbatch{8}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
    matlabbatch{8}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{8}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
    matlabbatch{9}.spm.spatial.coreg.estimate.ref(1) = cfg_dep('File Set Split: echos (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{9}.spm.spatial.coreg.estimate.source(1) = cfg_dep('File Set Split: echos (6)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{6}));
    matlabbatch{9}.spm.spatial.coreg.estimate.other(1) = cfg_dep('File Set Split: echos (7)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{7}));
    matlabbatch{9}.spm.spatial.coreg.estimate.other(2) = cfg_dep('File Set Split: field_maps (1)', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{9}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
    matlabbatch{9}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
    matlabbatch{9}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{9}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
    matlabbatch{10}.cfg_basicio.file_dir.file_ops.cfg_file_split.name = 'estimates_T1';
    matlabbatch{10}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('Coregister: Estimate: Coregistered Images', substruct('.','val', '{}',{7}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
    matlabbatch{10}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {1};
    matlabbatch{11}.cfg_basicio.file_dir.file_ops.cfg_file_split.name = 'estimated_PD';
    matlabbatch{11}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('Coregister: Estimate: Coregistered Images', substruct('.','val', '{}',{8}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
    matlabbatch{11}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {1};
    matlabbatch{12}.cfg_basicio.file_dir.file_ops.cfg_file_split.name = 'estimated_MT';
    matlabbatch{12}.cfg_basicio.file_dir.file_ops.cfg_file_split.files(1) = cfg_dep('Coregister: Estimate: Coregistered Images', substruct('.','val', '{}',{9}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
    matlabbatch{12}.cfg_basicio.file_dir.file_ops.cfg_file_split.index = {1};

    matlabbatch{13}.spm.spatial.coreg.write.ref(1) = cfg_dep('File Set Split: echos (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{13}.spm.spatial.coreg.write.source(1) = cfg_dep('File Set Split: estimated_PD (1)', substruct('.','val', '{}',{11}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{13}.spm.spatial.coreg.write.roptions.interp = 4;
    matlabbatch{13}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
    matlabbatch{13}.spm.spatial.coreg.write.roptions.mask = 0;
    matlabbatch{13}.spm.spatial.coreg.write.roptions.prefix = 'r';
    matlabbatch{14}.spm.spatial.coreg.write.ref(1) = cfg_dep('File Set Split: echos (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{14}.spm.spatial.coreg.write.source(1) = cfg_dep('File Set Split: estimated_MT (1)', substruct('.','val', '{}',{12}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{14}.spm.spatial.coreg.write.roptions.interp = 4;
    matlabbatch{14}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
    matlabbatch{14}.spm.spatial.coreg.write.roptions.mask = 0;
    matlabbatch{14}.spm.spatial.coreg.write.roptions.prefix = 'r';
    
    matlabbatch{15}.spm.spatial.preproc.channel(1).vols(1) = cfg_dep('File Set Split: echos (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{15}.spm.spatial.preproc.channel(1).biasreg = 0.0001;
    matlabbatch{15}.spm.spatial.preproc.channel(1).biasfwhm = 40;
    matlabbatch{15}.spm.spatial.preproc.channel(1).write = [0 1];
    matlabbatch{15}.spm.spatial.preproc.channel(2).vols(1) = cfg_dep('Coregister: Reslice: Resliced Images', substruct('.','val', '{}',{13}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rfiles'));
    matlabbatch{15}.spm.spatial.preproc.channel(2).biasreg = 0.0001;
    matlabbatch{15}.spm.spatial.preproc.channel(2).biasfwhm = 40;
    matlabbatch{15}.spm.spatial.preproc.channel(2).write = [0 1];
    matlabbatch{15}.spm.spatial.preproc.channel(3).vols(1) = cfg_dep('Coregister: Reslice: Resliced Images', substruct('.','val', '{}',{14}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rfiles'));
    matlabbatch{15}.spm.spatial.preproc.channel(3).biasreg = 0.0001;
    matlabbatch{15}.spm.spatial.preproc.channel(3).biasfwhm = 40;
    matlabbatch{15}.spm.spatial.preproc.channel(3).write = [0 1];
    matlabbatch{15}.spm.spatial.preproc.tissue(1).tpm = {'/data/underworld/home/kbas/spm12/tpm/TPM.nii,1'};
    matlabbatch{15}.spm.spatial.preproc.tissue(1).ngaus = 1;
    matlabbatch{15}.spm.spatial.preproc.tissue(1).native = [1 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(1).warped = [0 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(2).tpm = {'/data/underworld/home/kbas/spm12/tpm/TPM.nii,2'};
    matlabbatch{15}.spm.spatial.preproc.tissue(2).ngaus = 1;
    matlabbatch{15}.spm.spatial.preproc.tissue(2).native = [1 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(2).warped = [0 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(3).tpm = {'/data/underworld/home/kbas/spm12/tpm/TPM.nii,3'};
    matlabbatch{15}.spm.spatial.preproc.tissue(3).ngaus = 2;
    matlabbatch{15}.spm.spatial.preproc.tissue(3).native = [1 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(3).warped = [0 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(4).tpm = {'/data/underworld/home/kbas/spm12/tpm/TPM.nii,4'};
    matlabbatch{15}.spm.spatial.preproc.tissue(4).ngaus = 3;
    matlabbatch{15}.spm.spatial.preproc.tissue(4).native = [1 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(4).warped = [0 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(5).tpm = {'/data/underworld/home/kbas/spm12/tpm/TPM.nii,5'};
    matlabbatch{15}.spm.spatial.preproc.tissue(5).ngaus = 4;
    matlabbatch{15}.spm.spatial.preproc.tissue(5).native = [1 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(5).warped = [0 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(6).tpm = {'/data/underworld/home/kbas/spm12/tpm/TPM.nii,6'};
    matlabbatch{15}.spm.spatial.preproc.tissue(6).ngaus = 2;
    matlabbatch{15}.spm.spatial.preproc.tissue(6).native = [0 0];
    matlabbatch{15}.spm.spatial.preproc.tissue(6).warped = [0 0];
    matlabbatch{15}.spm.spatial.preproc.warp.mrf = 1;
    matlabbatch{15}.spm.spatial.preproc.warp.cleanup = 1;
    matlabbatch{15}.spm.spatial.preproc.warp.reg = [0 0.0002 0.1 0.01 0.04];
    matlabbatch{15}.spm.spatial.preproc.warp.affreg = 'mni';
    matlabbatch{15}.spm.spatial.preproc.warp.fwhm = 0;
    matlabbatch{15}.spm.spatial.preproc.warp.samp = 3;
    matlabbatch{15}.spm.spatial.preproc.warp.write = [0 0];
    matlabbatch{15}.spm.spatial.preproc.warp.vox = NaN;
    matlabbatch{15}.spm.spatial.preproc.warp.bb = [NaN NaN NaN
                                                   NaN NaN NaN];
    matlabbatch{16}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.name = 'processed_dir';
    matlabbatch{16}.cfg_basicio.file_dir.dir_ops.cfg_named_dir.dirs = {{['/data/underworld/home/kbas/03_data/processed_qmri_pd_2/' subject]}};
    matlabbatch{17}.spm.util.imcalc.input(1) = cfg_dep('Segment: c1 Images', substruct('.','val', '{}',{15}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','tiss', '()',{1}, '.','c', '()',{':'}));
    matlabbatch{17}.spm.util.imcalc.input(2) = cfg_dep('Segment: c2 Images', substruct('.','val', '{}',{15}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','tiss', '()',{2}, '.','c', '()',{':'}));
    matlabbatch{17}.spm.util.imcalc.input(3) = cfg_dep('Segment: c3 Images', substruct('.','val', '{}',{15}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','tiss', '()',{3}, '.','c', '()',{':'}));
    matlabbatch{17}.spm.util.imcalc.output = 'brain_mask';
    matlabbatch{17}.spm.util.imcalc.outdir(1) = cfg_dep('Named Directory Selector: processed_dir(1)', substruct('.','val', '{}',{16}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
    matlabbatch{17}.spm.util.imcalc.expression = '(i1+i2+i3)>0.25';
    matlabbatch{17}.spm.util.imcalc.var = struct('name', {}, 'value', {});
    matlabbatch{17}.spm.util.imcalc.options.dmtx = 0;
    matlabbatch{17}.spm.util.imcalc.options.mask = 0;
    matlabbatch{17}.spm.util.imcalc.options.interp = 1;
    matlabbatch{17}.spm.util.imcalc.options.dtype = 2;
    matlabbatch{18}.spm.tools.mb.fil.images(1) = cfg_dep('File Set Split: echos (1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('{}',{1}));
    matlabbatch{19}.spm.util.imcalc.input(1) = cfg_dep('Image Labelling: Labelled brains', substruct('.','val', '{}',{18}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','labels', '()',{':'}));
    matlabbatch{19}.spm.util.imcalc.output = 'amygdala_mask';
    matlabbatch{19}.spm.util.imcalc.outdir(1) = cfg_dep('Named Directory Selector: processed_dir(1)', substruct('.','val', '{}',{16}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
    matlabbatch{19}.spm.util.imcalc.expression = '(i1==31)+(i1==32)';
    matlabbatch{19}.spm.util.imcalc.var = struct('name', {}, 'value', {});
    matlabbatch{19}.spm.util.imcalc.options.dmtx = 0;
    matlabbatch{19}.spm.util.imcalc.options.mask = 0;
    matlabbatch{19}.spm.util.imcalc.options.interp = 1;
    matlabbatch{19}.spm.util.imcalc.options.dtype = 4;
    matlabbatch{20}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.files(1) = cfg_dep('Image Calculator: ImCalc Computed Image: amygdala_mask', substruct('.','val', '{}',{19}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{20}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.outdir(1) = cfg_dep('Named Directory Selector: processed_dir(1)', substruct('.','val', '{}',{16}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
    matlabbatch{20}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.keep = true;
    matlabbatch{21}.spm.util.imcalc.input(1) = cfg_dep('Image Labelling: Labelled brains', substruct('.','val', '{}',{18}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','labels', '()',{':'}));
    matlabbatch{21}.spm.util.imcalc.output = 'thalamus_mask';
    matlabbatch{21}.spm.util.imcalc.outdir(1) = cfg_dep('Named Directory Selector: processed_dir(1)', substruct('.','val', '{}',{16}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
    matlabbatch{21}.spm.util.imcalc.expression = '(i1==59)+(i1==60)';
    matlabbatch{21}.spm.util.imcalc.var = struct('name', {}, 'value', {});
    matlabbatch{21}.spm.util.imcalc.options.dmtx = 0;
    matlabbatch{21}.spm.util.imcalc.options.mask = 0;
    matlabbatch{21}.spm.util.imcalc.options.interp = 1;
    matlabbatch{21}.spm.util.imcalc.options.dtype = 4;
    matlabbatch{22}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.files(1) = cfg_dep('Image Calculator: ImCalc Computed Image: thalamus_mask', substruct('.','val', '{}',{21}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{22}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.outdir(1) = cfg_dep('Named Directory Selector: processed_dir(1)', substruct('.','val', '{}',{16}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','dirs', '{}',{1}));
    matlabbatch{22}.cfg_basicio.file_dir.file_ops.cfg_gzip_files.keep = true;

    spm_jobman('run',matlabbatch);
end

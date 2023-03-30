%-----------------------------------------------------------------------
% Job saved on 14-Dec-2021 17:38:05 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (12.6)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
cwd = pwd;
% matlabbatch{1}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000224-01.nii,1']};
% matlabbatch{1}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/115326/20210604/13/sMP03131-0013-00001-000224-01.nii,1']};
% matlabbatch{1}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/116284/20190412/13/sMP02645-0013-00001-000224-01.nii,1']};
matlabbatch{1}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/128221/20190920/13/sMP02820-0013-00001-000224-01.nii,1']};

% matlabbatch{1}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/10/sMP02874-0010-00001-000224-01.nii,1']};
% matlabbatch{1}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/115326/20210604/10/sMP03131-0010-00001-000224-01.nii,1']};
% matlabbatch{1}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/116284/20190412/10/sMP02645-0010-00001-000224-01.nii,1']};
matlabbatch{1}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/128221/20190920/10/sMP02820-0010-00001-000224-01.nii,1']};

matlabbatch{1}.spm.spatial.coreg.write.roptions.interp = 4;
matlabbatch{1}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
matlabbatch{1}.spm.spatial.coreg.write.roptions.mask = 0;
matlabbatch{1}.spm.spatial.coreg.write.roptions.prefix = 'r';
% matlabbatch{2}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000224-01.nii,1']};
% matlabbatch{2}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/115326/20210604/13/sMP03131-0013-00001-000224-01.nii,1']};
% matlabbatch{2}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/116284/20190412/13/sMP02645-0013-00001-000224-01.nii,1']};
matlabbatch{2}.spm.spatial.coreg.write.ref = {['/data/underworld/kbas/03_data/source/mri/128221/20190920/13/sMP02820-0013-00001-000224-01.nii,1']};

% matlabbatch{2}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/16/sMP02874-0016-00001-000224-01.nii,1']};
% matlabbatch{2}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/115326/20210604/16/sMP03131-0016-00001-000224-01.nii,1']};
% matlabbatch{2}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/116284/20190412/16/sMP02645-0016-00001-000224-01.nii,1']};
matlabbatch{2}.spm.spatial.coreg.write.source = {['/data/underworld/kbas/03_data/source/mri/128221/20190920/16/sMP02820-0016-00001-000224-01.nii,1']};

matlabbatch{2}.spm.spatial.coreg.write.roptions.interp = 4;
matlabbatch{2}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
matlabbatch{2}.spm.spatial.coreg.write.roptions.mask = 0;
matlabbatch{2}.spm.spatial.coreg.write.roptions.prefix = 'r';
% matlabbatch{3}.spm.spatial.preproc.channel(1).vols = {['/data/underworld/kbas/03_data/source/mri/112111/20191115/13/sMP02874-0013-00001-000224-01.nii,1']};
% matlabbatch{3}.spm.spatial.preproc.channel(1).vols = {['/data/underworld/kbas/03_data/source/mri/115326/20210604/13/sMP03131-0013-00001-000224-01.nii,1']};
% matlabbatch{3}.spm.spatial.preproc.channel(1).vols = {['/data/underworld/kbas/03_data/source/mri/116284/20190412/13/sMP02645-0013-00001-000224-01.nii,1']};
matlabbatch{3}.spm.spatial.preproc.channel(1).vols = {['/data/underworld/kbas/03_data/source/mri/128221/20190920/13/sMP02820-0013-00001-000224-01.nii,1']};
matlabbatch{3}.spm.spatial.preproc.channel(1).biasreg = 0.0001;
matlabbatch{3}.spm.spatial.preproc.channel(1).biasfwhm = 40;
matlabbatch{3}.spm.spatial.preproc.channel(1).write = [0 1];
matlabbatch{3}.spm.spatial.preproc.channel(2).vols(1) = cfg_dep('Coregister: Reslice: Resliced Images', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rfiles'));
matlabbatch{3}.spm.spatial.preproc.channel(2).biasreg = 0.0001;
matlabbatch{3}.spm.spatial.preproc.channel(2).biasfwhm = 40;
matlabbatch{3}.spm.spatial.preproc.channel(2).write = [0 1];
matlabbatch{3}.spm.spatial.preproc.channel(3).vols(1) = cfg_dep('Coregister: Reslice: Resliced Images', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rfiles'));
matlabbatch{3}.spm.spatial.preproc.channel(3).biasreg = 0.0001;
matlabbatch{3}.spm.spatial.preproc.channel(3).biasfwhm = 40;
matlabbatch{3}.spm.spatial.preproc.channel(3).write = [0 1];
matlabbatch{3}.spm.spatial.preproc.tissue(1).tpm = {'/data/underworld/kbas/spm12/tpm/TPM.nii,1'};
matlabbatch{3}.spm.spatial.preproc.tissue(1).ngaus = 1;
matlabbatch{3}.spm.spatial.preproc.tissue(1).native = [1 0];
matlabbatch{3}.spm.spatial.preproc.tissue(1).warped = [0 0];
matlabbatch{3}.spm.spatial.preproc.tissue(2).tpm = {'/data/underworld/kbas/spm12/tpm/TPM.nii,2'};
matlabbatch{3}.spm.spatial.preproc.tissue(2).ngaus = 1;
matlabbatch{3}.spm.spatial.preproc.tissue(2).native = [1 0];
matlabbatch{3}.spm.spatial.preproc.tissue(2).warped = [0 0];
matlabbatch{3}.spm.spatial.preproc.tissue(3).tpm = {'/data/underworld/kbas/spm12/tpm/TPM.nii,3'};
matlabbatch{3}.spm.spatial.preproc.tissue(3).ngaus = 2;
matlabbatch{3}.spm.spatial.preproc.tissue(3).native = [1 0];
matlabbatch{3}.spm.spatial.preproc.tissue(3).warped = [0 0];
matlabbatch{3}.spm.spatial.preproc.tissue(4).tpm = {'/data/underworld/kbas/spm12/tpm/TPM.nii,4'};
matlabbatch{3}.spm.spatial.preproc.tissue(4).ngaus = 3;
matlabbatch{3}.spm.spatial.preproc.tissue(4).native = [1 0];
matlabbatch{3}.spm.spatial.preproc.tissue(4).warped = [0 0];
matlabbatch{3}.spm.spatial.preproc.tissue(5).tpm = {'/data/underworld/kbas/spm12/tpm/TPM.nii,5'};
matlabbatch{3}.spm.spatial.preproc.tissue(5).ngaus = 4;
matlabbatch{3}.spm.spatial.preproc.tissue(5).native = [1 0];
matlabbatch{3}.spm.spatial.preproc.tissue(5).warped = [0 0];
matlabbatch{3}.spm.spatial.preproc.tissue(6).tpm = {'/data/underworld/kbas/spm12/tpm/TPM.nii,6'};
matlabbatch{3}.spm.spatial.preproc.tissue(6).ngaus = 2;
matlabbatch{3}.spm.spatial.preproc.tissue(6).native = [0 0];
matlabbatch{3}.spm.spatial.preproc.tissue(6).warped = [0 0];
matlabbatch{3}.spm.spatial.preproc.warp.mrf = 1;
matlabbatch{3}.spm.spatial.preproc.warp.cleanup = 1;
matlabbatch{3}.spm.spatial.preproc.warp.reg = [0 0.0002 0.1 0.01 0.04];
matlabbatch{3}.spm.spatial.preproc.warp.affreg = 'mni';
matlabbatch{3}.spm.spatial.preproc.warp.fwhm = 0;
matlabbatch{3}.spm.spatial.preproc.warp.samp = 3;
matlabbatch{3}.spm.spatial.preproc.warp.write = [0 0];
matlabbatch{3}.spm.spatial.preproc.warp.vox = NaN;
matlabbatch{3}.spm.spatial.preproc.warp.bb = [NaN NaN NaN
                                              NaN NaN NaN];
matlabbatch{4}.spm.util.imcalc.input(1) = cfg_dep('Segment: c1 Images', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','tiss', '()',{1}, '.','c', '()',{':'}));
matlabbatch{4}.spm.util.imcalc.input(2) = cfg_dep('Segment: c2 Images', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','tiss', '()',{2}, '.','c', '()',{':'}));
matlabbatch{4}.spm.util.imcalc.input(3) = cfg_dep('Segment: c3 Images', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','tiss', '()',{3}, '.','c', '()',{':'}));
matlabbatch{4}.spm.util.imcalc.output = 'brain_mask';
% matlabbatch{4}.spm.util.imcalc.outdir = {''};
% matlabbatch{4}.spm.util.imcalc.outdir = {'/data/underworld/kbas/03_data/derivatives/112111/20191115/anat/spm-qmap-preproc'};
% matlabbatch{4}.spm.util.imcalc.outdir = {'/data/underworld/kbas/03_data/derivatives/115326/20210604/anat/spm-qmap-preproc'};
% matlabbatch{4}.spm.util.imcalc.outdir = {'/data/underworld/kbas/03_data/derivatives/116284/20190412/anat/spm-qmap-preproc'};
matlabbatch{4}.spm.util.imcalc.outdir = {'/data/underworld/kbas/03_data/derivatives/128221/20190920/anat/spm-qmap-preproc'};

matlabbatch{4}.spm.util.imcalc.expression = '(i1+i2+i3)>0.25';
matlabbatch{4}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{4}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{4}.spm.util.imcalc.options.mask = 0;
matlabbatch{4}.spm.util.imcalc.options.interp = 1;
matlabbatch{4}.spm.util.imcalc.options.dtype = 2;

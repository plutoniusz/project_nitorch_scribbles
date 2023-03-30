% List of open inputs
nrun = X; % enter the number of runs here
jobfile = {'/data/underworld/home/kbas/project_nitorch_scribbles/112111_mask_creation_new_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(0, nrun);
for crun = 1:nrun
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});

#! /bin/bash
matlab -batch "qmri_preproc"
if [ $? -ne 0 ]; then
  exit 1
fi
echo
echo "preprocessing done"
echo
python /data/underworld/kbas/project_nitorch_scribbles/qmri_code/estimate_predict.py
if [ $? -ne 0 ]; then
  exit 1
fi
echo
echo "estimate_predict.py done"
echo
python /data/underworld/kbas/project_nitorch_scribbles/qmri_code/validate.py
if [ $? -ne 0 ]; then
  exit 1
fi
echo
echo "validate.py done"
echo
python /data/underworld/kbas/project_nitorch_scribbles/qmri_code/bar_plot_sum.py
if [ $? -ne 0 ]; then
  exit 1
fi
echo
echo "bar_plot_sum.py done"
echo

from typing import OrderedDict, Any, Optional
import colibri


def task_roi_means(task: OrderedDict[str, Any],
                   named_obj: dict[str, Any]):
    """Run the ROIMeans task. Loads an image series and a ROI image, and
    computes mean voxel values for each ROI in each time frame. The result
    is saved as a table to named_obj.
    The input to the function is an xml structure, which must have the
    following structure (not ordered):

    <img_path>PATH_TO_IMAGE_SERIES</img_path>
    <roi_path>PATH_TO_ROI_IMAGE_FILE</roi_path>
    <labels>ROI_LABEL_1,NEW_LABEL_1;
            ROI_LABEL_2,NEW_LABEL_2;...</labels> <!-- OPTIONAL -->
    <ignore>LABEL_1,LABEL_2,...</ignore> <!-- OPTIONAL -->
    <resample>img_OR_roi</resample> <!-- OPTIONAL -->
    <frame_dur>true_OR_false</frame_dur> <!-- OPTIONAL -->
    <res_name>TABLE_KEY_IN_NAMED_OBJ</res_name>

    With the <labels>-tag, new labels can be chosen if the ROI-labels in the
    ROI-file are not descriptive.
    The <ignore> tag can be used to avoid computing roi-means for certain
    labels.
    The <resample>-tag can be used to resample either the images in the
    series to the ROI image (use the value 'img') or the other way around
    (use the value 'roi'). This is a mandatory input if the two images are
    not in the same physical space.
    The <frame_dur>-tag can be used to also output the frame duration for each
    frame. If the tag is not included, the frame duration will be ignored and
    only relative acquisition times are output.
    """

    print("Starting image read and ROI-mean calculation.")

    # Get the image and output paths
    img_path = str(task['img_path'])
    roi_path = str(task['roi_path'])
    res_name = str(task['res_name'])

    # Create label dictionary
    labels = {}
    if 'labels' in task:
        # This section transforms the string "X,a;Y,b;Z,c" into a dict of the
        # form {'X': 'a', 'Y': 'b', 'Z': 'c'}
        label_string = str(task['labels']).split(';')
        for label in label_string:
            label_split = label.split(',')
            labels[label_split[0]] = label_split[1]

    # Create ignore list
    if 'ignore' in task:
        # This section transforms the string "a,b,c" into a list of the
        # form ['a','b','c']
        ignore = task['ignore'].split(',')
    else:
        ignore = []

    # Check if resampling is required
    resample: Optional[str] = None
    if 'resample' in task:
        resample = str(task['resample'])

    # Check if frame duration should be included
    frame_dur = False
    if 'frame_dur' in task:
        if task['frame_dur'] == 'true':
            frame_dur = True

    print("Reading images from ", img_path, ".")
    print("Reading ROI image from ", roi_path, ".")
    print("Processing...")
    # Run the task!
    dyn = colibri.lazy_series_roi_means(img_path,
                                        roi_path,
                                        resample=resample,
                                        labels=labels,
                                        ignore=ignore,
                                        frame_dur=frame_dur)
    print("... done!")
    print()

    print("Storing result as ", res_name, " in named_obj...")
    # Put result in named_obj
    named_obj[res_name] = dyn
    print("... done!")
    print()

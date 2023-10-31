import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/dialogs/file_picker_dialog.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/update_garden_task/update_garden_task_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/ui/widgets/b_agri/attach_file/attach_file_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/attach_file/pick_file_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/farmer_picker/app_farmer_picker.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/step_picker/app_step_picker.dart';
import 'package:flutter_base/utils/dialog_utils.dart';

import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/intl.dart';

class UpdateGardenTaskPage extends StatefulWidget {
  final String? name;
  final String? task_id;
  final String? season_id;

  UpdateGardenTaskPage({Key? key, this.name, this.task_id, this.season_id})
      : super(key: key);

  @override
  _UpdateGardenTaskPageState createState() => _UpdateGardenTaskPageState();
}

class _UpdateGardenTaskPageState extends State<UpdateGardenTaskPage> {
  final _formKey = GlobalKey<FormState>();
  final descriptionController = TextEditingController(text: "");
  late TextEditingController dateController;

  late StepPickerController stepController;
  late FarmerPickerController farmerController;
  late TextEditingController startHourController;
  late TextEditingController startMinuteController;
  late TextEditingController endHourController;
  late TextEditingController endMinuteController;
  late TextEditingController itemsController;

  AppCubit? _appCubit;
  late UpdateGardenTaskCubit _cubit;

  @override
  void initState() {
    super.initState();
    _appCubit = BlocProvider.of<AppCubit>(context);
    _cubit = BlocProvider.of<UpdateGardenTaskCubit>(context);

    _cubit.getTaskDetail(widget.task_id!);

    var now = new DateTime.now();
    var formatter = new DateFormat('yyyy-MM-dd');
    String formattedDate = formatter.format(now);

    //Set initial cubit
    dateController = TextEditingController(text: formattedDate);
    stepController = StepPickerController();
    farmerController = FarmerPickerController();
    startHourController = TextEditingController();
    startMinuteController = TextEditingController();
    endHourController = TextEditingController();
    endMinuteController = TextEditingController();
    itemsController = TextEditingController();

    _cubit.changeDate(formattedDate);
    _cubit.changeSeason(widget.season_id);
    _cubit.changeManager(GlobalData.instance.userEntity!.id);
    _cubit.changeDescription(descriptionController.text);
    _cubit.changeItems(itemsController.text);

    descriptionController.addListener(() {
      _cubit.changeDescription(descriptionController.text);
    });
    itemsController.addListener(() {
      _cubit.changeItems(itemsController.text);
    });
    stepController.addListener(() {
      _cubit.changeStep(stepController.stepEntity);
    });
    farmerController.addListener(() {
      _cubit.changeFarmer(farmerController.farmerList);
    });

    startHourController.addListener(() {
      _cubit.changeStartHour(startHourController.text);
    });

    startMinuteController.addListener(() {
      _cubit.changeStartMinute(startMinuteController.text);
    });

    endHourController.addListener(() {
      _cubit.changeEndHour(endHourController.text);
    });

    endMinuteController.addListener(() {
      _cubit.changeEndMinute(endMinuteController.text);
    });
  }

  @override
  void dispose() {
    super.dispose();
    dateController.dispose();
    stepController.dispose();
    farmerController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Chỉnh sửa công việc',
      ),
      body: Padding(
        padding: EdgeInsets.only(top: 10, right: 20, left: 20),
        child: SingleChildScrollView(
          child: Column(
            children: [
              Text(
                '${widget.name}: ${dateController.text}',
                style: AppTextStyle.tintS14,
              ),
              SizedBox(height: 20),
              BlocConsumer<UpdateGardenTaskCubit, UpdateGardenTaskState>(
                listenWhen: (prev, current) =>
                    prev.loadDetailStatus != current.loadDetailStatus,
                listener: (context, state) {
                  stepController.stepEntity = state.step;
                  descriptionController.text = state.description ?? "";
                  farmerController.farmerList = state.farmers;
                  startHourController.text = state.startHour ?? "";
                  startMinuteController.text = state.startMinute ?? "";
                  endHourController.text = state.endHour ?? "";
                  endMinuteController.text = state.endMinute ?? "";
                  itemsController.text = state.items ?? "";
                },
                builder: (context, state) {
                  return Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Bước',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        AppPageStepPicker(
                          seasonId: widget.season_id ?? "",
                          controller: stepController,
                          onChanged: (value) {
                            _cubit.changeStep(value);
                          },
                        ),
                        SizedBox(height: 25),
                        Text(
                          'Công việc phát sinh',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        AppTextField(
                          autoValidateMode: AutovalidateMode.onUserInteraction,
                          controller: descriptionController,
                        ),
                        SizedBox(height: 25),
                        Row(
                          children: [
                            Text(
                              'Thời gian:',
                              style: AppTextStyle.greyS14,
                            ),
                            SizedBox(width: 30),
                            Text(
                              'từ',
                              style: AppTextStyle.greyS14,
                            ),
                            SizedBox(width: 8),
                            _buildTimeTextField(true, startHourController),
                            SizedBox(width: 4),
                            Text(
                              ':',
                              style: AppTextStyle.greyS14,
                            ),
                            SizedBox(width: 4),
                            _buildTimeTextField(false, startMinuteController),
                            SizedBox(width: 8),
                            Text(
                              'đến',
                              style: AppTextStyle.greyS14,
                            ),
                            SizedBox(width: 8),
                            _buildTimeTextField(true, endHourController),
                            SizedBox(width: 4),
                            Text(
                              ':',
                              style: AppTextStyle.greyS14,
                            ),
                            SizedBox(width: 4),
                            _buildTimeTextField(false, endMinuteController),
                            Expanded(child: SizedBox())
                          ],
                        ),
                        SizedBox(height: 25),
                        Text(
                          'Người thực hiện',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        AppPageFarmerPicker(
                          controller: farmerController,
                          onChanged: (value) {
                            _cubit.changeFarmer(value);
                          },
                        ),
                        SizedBox(height: 25),
                        Text(
                          'Vật tư sử dụng',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        AppTextField(
                          autoValidateMode: AutovalidateMode.onUserInteraction,
                          controller: itemsController,
                        ),
                        SizedBox(height: 25),
                        Text(
                          'Kết quả công việc',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        _buildPickFileButton(),
                        _buildAttachedFileWidget(),
                        SizedBox(height: 40),
                        _buildActionCreate(context),
                        SizedBox(height: 20),
                      ],
                    ),
                  );
                },
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPickFileButton() {
    return BlocBuilder<UpdateGardenTaskCubit, UpdateGardenTaskState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return prev.uploadFileStatus != current.uploadFileStatus ||
            prev.removeFileStatus != current.removeFileStatus;
      },
      builder: (context, state) {
        bool isFull = (state.files ?? []).length >= AppConfig.maxAttachFile;
        return isFull
            ? Container()
            : PickFileWidget(
                isLoading: state.uploadFileStatus == LoadStatus.LOADING,
                onPressed: () async {
                  FileInfo? file = await DialogUtils.pickFile(context);
                  if (file?.file != null) {
                    _cubit.uploadFile(file?.file);
                  }
                },
              );
      },
    );
  }

  Widget _buildAttachedFileWidget() {
    return BlocBuilder<UpdateGardenTaskCubit, UpdateGardenTaskState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return prev.uploadFileStatus != current.uploadFileStatus ||
            prev.removeFileStatus != current.removeFileStatus;
      },
      builder: (context, state) {
        List<Widget> widgets = [];
        final filePaths = _cubit.state.result ?? [];
        for (int i = 0; i < filePaths.length; i++) {
          widgets.add(AttachedFileWidget(
            filePath: filePaths[i],
            onDeletePressed: () {
              _cubit.removeFileAtIndex(i);
            },
          ));
        }
        return Wrap(
          spacing: 20,
          alignment: WrapAlignment.start,
          crossAxisAlignment: WrapCrossAlignment.start,
          children: List.generate(
            widgets.length,
            (index) {
              return widgets[index];
            },
          ),
        );
      },
    );
  }

  Widget _buildActionCreate(BuildContext context) {
    return BlocConsumer<UpdateGardenTaskCubit, UpdateGardenTaskState>(
      bloc: _cubit,
      listenWhen: (prev, current) {
        return prev.updateGardenTaskStatus != current.updateGardenTaskStatus;
      },
      listener: (context, state) {
        if (state.updateGardenTaskStatus == LoadStatus.SUCCESS) {
          _showCreateSuccess();
        }
        if (state.updateGardenTaskStatus == LoadStatus.FAILURE) {
          showSnackBar('Có lỗi xảy ra!');
        }
      },
      builder: (context, state) {
        final isLoading = (state.updateGardenTaskStatus == LoadStatus.LOADING);
        return Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AppButton(
              color: AppColors.redButton,
              title: 'Hủy bỏ',
              onPressed: () {
                Navigator.of(context).pop(false);
              },
            ),
            SizedBox(width: 50),
            AppButton(
              width: 100,
              color: AppColors.main,
              title: 'Xác nhận',
              onPressed: () async {
                if (_formKey.currentState!.validate()) {
                  _cubit.updateTask(widget.task_id);
                }
              },
              isLoading: isLoading,
            ),
          ],
        );
      },
    );
  }

  void _showCreateSuccess() async {
    showSnackBar('Cập nhật thành công!');
    Navigator.of(context).pop(true);
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }

  _buildTimeTextField(bool validateHour, TextEditingController controller) {
    return Container(
      width: 20,
      child: TextFormField(
        controller: controller,
        keyboardType: TextInputType.number,
        autovalidateMode: AutovalidateMode.onUserInteraction,
        validator: (value) {
          if (Validator.validate0to9Character(value!)) if (int.parse(value) >
              (validateHour ? 23 : 59))
            return '';
          else
            return null;
          else
            return '';
        },
        textAlign: TextAlign.center,
        inputFormatters: [LengthLimitingTextInputFormatter(2)],
        maxLengthEnforcement: MaxLengthEnforcement.enforced,
        decoration: InputDecoration(
            isDense: true,
            errorBorder:
                UnderlineInputBorder(borderSide: BorderSide(color: Colors.red)),
            focusedErrorBorder:
                UnderlineInputBorder(borderSide: BorderSide(color: Colors.red)),
            errorStyle: TextStyle(height: 0),
            enabledBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Color(0xFF000000)),
            ),
            focusedBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Color(0xFF000000)),
            ),
            contentPadding: EdgeInsets.only(bottom: 0, top: 0)),
      ),
    );
  }
}

class GardenTaskUpdateArgument {
  String? name;
  String? task_id;
  String? season_id;

  GardenTaskUpdateArgument({
    this.name,
    this.task_id,
    this.season_id,
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/models/entities/process/stage_entity.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/process_management/process_season/process_season_cubit.dart';
import 'package:flutter_base/ui/pages/process_management/widget/modal_add_step_widget.dart';
import 'package:flutter_base/ui/pages/process_management/widget/modal_edit_step_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/multiple_tree_picker/app_tree_picker.dart';

import 'package:flutter_base/utils/validators.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class UpdateProcessSeasonPage extends StatefulWidget {
  final String? process_id;

  UpdateProcessSeasonPage({Key? key, this.process_id}) : super(key: key);

  @override
  _UpdateProcessSeasonPageState createState() =>
      _UpdateProcessSeasonPageState();
}

class _UpdateProcessSeasonPageState extends State<UpdateProcessSeasonPage> {
  final _formKey = GlobalKey<FormState>();
  List<PhaseProcess> listPhase = [];
  TreePickerController treeController = TreePickerController();
  TextEditingController nameController = TextEditingController(text: '');

  ProcessSeasonCubit? _cubit;

  @override
  void initState() {
    super.initState();
    _cubit = BlocProvider.of<ProcessSeasonCubit>(context);

    // Set initial cubit
    _cubit!.changeName(nameController.text);
    nameController.addListener(() {
      _cubit!.changeName(nameController.text);
    });

    _cubit!.getProcessDetail(widget.process_id!);
  }

  @override
  void dispose() {
    _cubit!.close();
    nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBarWidget(
        context: context,
        title: 'Sửa quy trình',
      ),
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        Text(
                          'Tên quy trình',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        BlocConsumer<ProcessSeasonCubit, ProcessSeasonState>(
                          listener: (context, state) {
                            if (state.loadDetailStatus == LoadStatus.SUCCESS) {
                              nameController = TextEditingController(
                                  text: _cubit!.state.name);
                            }
                            // TODO: implement listener
                          },
                          builder: (context, state) {
                            return AppTextField(
                              autoValidateMode:
                                  AutovalidateMode.onUserInteraction,
                              hintText: 'Nhập vào tên quy trình',
                              controller: nameController,
                              validator: (value) {
                                if (Validator.validateNullOrEmpty(value!))
                                  return "Chưa nhập tên quy trình";
                                else
                                  return null;
                              },
                            );
                          },
                        ),
                        SizedBox(height: 20),
                        Text(
                          'Các loại cây trồng áp dụng',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        BlocConsumer<ProcessSeasonCubit, ProcessSeasonState>(
                          listener: (context, state) {
                            if (state.loadDetailStatus == LoadStatus.SUCCESS) {
                              treeController = TreePickerController(
                                  treeList: _cubit!.state.trees);
                            }
                            // TODO: implement listener
                          },
                          builder: (context, state) => AppPageTreePicker(
                            controller: treeController,
                            onChanged: (value) {
                              _cubit?.changeTree(value);
                            },
                          ),
                        ),
                        SizedBox(height: 20),
                        Text(
                          'Các giai đoạn chăm sóc',
                          style: AppTextStyle.greyS14,
                        ),
                        SizedBox(height: 10),
                        BlocBuilder<ProcessSeasonCubit, ProcessSeasonState>(
                          builder: (context, state) {
                            return Visibility(
                              visible:
                                  state.stages!.length >= AppConfig.stagesLength
                                      ? false
                                      : true,
                              child: Padding(
                                padding: const EdgeInsets.only(left: 140),
                                child: AppButton(
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text('Thêm giai đoạn'),
                                      FittedBox(
                                          child: Icon(
                                        Icons.add,
                                        color: Color(0xFF373737),
                                      )),
                                    ],
                                  ),
                                  color: Color(0xFF8FE192),
                                  height: 30,
                                  width: double.infinity,
                                  onPressed: () {
                                    _cubit?.addList(StageEntity());
                                  },
                                ),
                              ),
                            );
                          },
                        ),
                        SizedBox(height: 20),
                        BlocBuilder<ProcessSeasonCubit, ProcessSeasonState>(
                          builder: (context, state) {
                            if (state.loadDetailStatus == LoadStatus.LOADING) {
                              return Center(
                                  child: CircularProgressIndicator(
                                color: AppColors.main,
                              ));
                            } else if (state.loadDetailStatus ==
                                LoadStatus.FAILURE) {
                              return Container();
                            } else if (state.loadDetailStatus ==
                                LoadStatus.SUCCESS) {
                              return state.stages!.length != 0
                                  ? Column(
                                      children: List.generate(
                                          state.stages!.length,
                                          (index) => PhaseProcess(
                                                index: index,
                                                cubitProcess: _cubit!,
                                                phase: '${index + 1}',
                                                onRemove: () {
                                                  _cubit!.removeList(index);
                                                },
                                              )),
                                    )
                                  : Container();
                            } else {
                              return Container();
                            }
                          },
                        ),
                      ],
                    ),
                  ),
                ),
                SizedBox(
                  height: 20,
                ),
                buildActionCreate(context),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget buildActionCreate(BuildContext context) {
    return BlocConsumer<ProcessSeasonCubit, ProcessSeasonState>(
      bloc: _cubit,
      listenWhen: (prev, current) {
        return prev.updateProcessSeasonStatus !=
            current.updateProcessSeasonStatus;
      },
      listener: (context, state) {
        if (state.updateProcessSeasonStatus == LoadStatus.SUCCESS) {
          _showCreateSuccess();
        }
        if (state.updateProcessSeasonStatus == LoadStatus.FAILURE) {
          showSnackBar('Có lỗi xảy ra!');
        }
      },
      builder: (context, state) {
        final isLoading =
            (state.updateProcessSeasonStatus == LoadStatus.LOADING);
        return Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
              child: AppButton(
                color: AppColors.redButton,
                title: 'Hủy bỏ',
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ),
            SizedBox(width: 40),
            Expanded(
              child: AppButton(
                width: 100,
                color: AppColors.main,
                title: 'Xác nhận',
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _cubit?.updateProcess(widget.process_id);
                  }
                },
                isLoading: isLoading,
              ),
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
}

class PhaseProcess extends StatefulWidget {
  int? index;
  String? phase;
  VoidCallback? onRemove;
  ProcessSeasonCubit cubitProcess;

  PhaseProcess(
      {Key? key,
      this.index,
      this.phase,
      this.onRemove,
      required this.cubitProcess})
      : super(key: key);

  @override
  State<PhaseProcess> createState() => _PhaseProcessState();
}

class _PhaseProcessState extends State<PhaseProcess> {
  @override
  Widget build(BuildContext context) {
    int sumStart = 0;
    int sumEnd = 0;
    if (widget.cubitProcess.state.stages![widget.index!].steps != null) {
      for (int i = 0;
          i < widget.cubitProcess.state.stages![widget.index!].steps!.length;
          i++) {
        var a = widget.cubitProcess.state.stages![widget.index!].steps;
        sumStart += a![i].from_day!;
        sumEnd += a[i].to_day!;
      }
    }

    return Column(
      children: [
        Container(
          width: double.infinity,
          margin: EdgeInsets.only(left: 2, right: 2, bottom: 30),
          decoration: BoxDecoration(
            color: Colors.white,
          ),
          child: Stack(children: [
            Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    height: 40,
                    width: double.infinity,
                    padding: EdgeInsets.all(5),
                    decoration: BoxDecoration(
                      color: AppColors.colors[widget.index!],
                      borderRadius: BorderRadius.circular(3),
                    ),
                    child: Row(
                      children: [
                        Text(
                          'Giai đoạn ${widget.phase}',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        Text(
                          'Thời gian: ',
                          style: TextStyle(
                            color: Color(0xFFBBB5D4),
                            fontSize: 14,
                          ),
                        ),
                        Text(
                          '$sumStart - $sumEnd ngày',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),
                  SizedBox(
                    height: 5,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(
                        flex: 3,
                        child: Container(
                          child: Column(
                            children: [
                              SizedBox(
                                height: 5,
                              ),
                              BlocBuilder<ProcessSeasonCubit,
                                  ProcessSeasonState>(
                                buildWhen: (prev, current) =>
                                    prev.actionWithStepStatus !=
                                    current.actionWithStepStatus,
                                builder: (context, state) {
                                  return Column(
                                    children: List.generate(
                                        state.stages![widget.index!].steps
                                                ?.length ??
                                            0, (index) {
                                      return StepWidget(
                                          index: index,
                                          indexStages: widget.index!,
                                          phase: widget.phase,
                                          cubitProcess: widget.cubitProcess,
                                          step: state.stages![widget.index!]
                                              .steps![index]);
                                    }),
                                  );
                                },
                              ),
                              Padding(
                                padding: const EdgeInsets.only(left: 180),
                                child: AppButton(
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text('Thêm bước'),
                                      FittedBox(
                                          child: Icon(
                                        Icons.add,
                                        color: Color(0xFF373737),
                                      )),
                                    ],
                                  ),
                                  color: Color(0xFFDDDAEA),
                                  height: 37,
                                  border: 10,
                                  width: double.infinity,
                                  onPressed: () {
                                    showModalBottomSheet(
                                      isDismissible: false,
                                      context: context,
                                      isScrollControlled: true,
                                      backgroundColor: Colors.transparent,
                                      shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.only(
                                              topLeft:
                                                  const Radius.circular(20),
                                              topRight:
                                                  const Radius.circular(20))),
                                      builder: (context) => ModalAddStepWidget(
                                        phase: widget.phase ?? "",
                                        onPressed:
                                            (name, startDate, endDate, stepId) {
                                          StepEntity step = StepEntity(
                                              name: name,
                                              from_day: int.parse(startDate),
                                              to_day: int.parse(endDate));

                                          widget.cubitProcess
                                              .createStep(widget.index!, step);
                                        },
                                      ),
                                    );
                                  },
                                ),
                              ),
                            ],
                          ),
                        ),
                      )
                    ],
                  )
                ]),
            GestureDetector(
              onTap: widget.onRemove,
              child: Align(
                alignment: Alignment.topRight,
                child: Container(
                  height: 30,
                  padding: EdgeInsets.only(top: 7, right: 5),
                  child: FittedBox(
                    child: Icon(
                      Icons.close,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ),
          ]),
        ),
        SizedBox(
          height: 10,
        )
      ],
    );
  }
}

class StepWidget extends StatefulWidget {
  final int? index;
  final StepEntity? step;
  final String? phase;
  final int? indexStages;
  final ProcessSeasonCubit cubitProcess;

  const StepWidget({
    Key? key,
    required this.index,
    this.indexStages,
    this.step,
    this.phase,
    required this.cubitProcess,
  }) : super(key: key);

  @override
  State<StepWidget> createState() => _StepWidgetState();
}

class _StepWidgetState extends State<StepWidget> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        showModalBottomSheet(
          isDismissible: false,
          context: context,
          isScrollControlled: true,
          backgroundColor: Colors.transparent,
          shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(20),
                  topRight: const Radius.circular(20))),
          builder: (context) => ModalEditStepWidget(
            phase: widget.phase ?? "",
            name: widget.step!.name,
            stepId: widget.step!.step_id,
            startDate: widget.step!.from_day!.toString(),
            endDate: widget.step!.to_day!.toString(),
            actualDay: (widget.step!.actual_day) != null
                ? widget.step!.actual_day.toString()
                : "",
            onPressed: (name, startDate, endDate, stepId, actualDay) {
              String? id;
              if (stepId == null) {
                id = null;
              } else {
                if (stepId.isEmpty) {
                  id = null;
                } else {
                  id = stepId;
                }
              }
              StepEntity step = StepEntity(
                name: name,
                step_id: id,
                from_day: int.parse(startDate),
                to_day: int.parse(endDate),
                actual_day: int.parse(actualDay),
              );

              widget.cubitProcess
                  .editSteps(widget.index!, widget.indexStages!, step);
            },
            onDelete: () {
              widget.cubitProcess
                  .removeStep(widget.index!, widget.indexStages!);
            },
          ),
        );
      },
      child: Container(
        padding: EdgeInsets.all(10),
        margin: EdgeInsets.only(bottom: 10),
        decoration: BoxDecoration(
            color: Color(0xFFDDDAEA),
            borderRadius: BorderRadius.all(Radius.circular(10))),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  widget.step!.name ?? '',
                  style: TextStyle(
                    color: Colors.black87,
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Row(
                  children: [
                    Text('Từ'),
                    SizedBox(
                      width: 3,
                    ),
                    Text(
                      '${widget.step!.from_day}',
                    ),
                    SizedBox(
                      width: 2,
                    ),
                    Text('-'),
                    SizedBox(
                      width: 2,
                    ),
                    Text('${widget.step!.to_day}'),
                    SizedBox(
                      width: 3,
                    ),
                    Text('ngày'),
                  ],
                )
              ],
            ),
            SizedBox(
              height: 5,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                Text(
                  (widget.step!.actual_day) != null
                      ? 'Thời gian thực hiện ${widget.step!.actual_day} ngày'
                      : 'Thời gian thực hiện dự kiến ${widget.step!.from_day} ngày',
                  style: TextStyle(
                    color: Color(0xFF9E7F2F),
                  ),
                )
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class ProcessSeasonArgument {
  String? process_id;

  ProcessSeasonArgument({
    this.process_id,
  });
}

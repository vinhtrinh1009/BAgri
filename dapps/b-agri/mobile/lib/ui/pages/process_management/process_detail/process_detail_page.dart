import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/process_management/process_detail/process_detail_cubit.dart';
import 'package:flutter_base/ui/pages/process_management/update_process/update_process_page.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/multiple_tree_picker/app_tree_picker.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

class ProcessDetailPage extends StatefulWidget {
  final String? process_id;

  ProcessDetailPage({Key? key, this.process_id}) : super(key: key);

  @override
  _ProcessDetailPageState createState() => _ProcessDetailPageState();
}

class _ProcessDetailPageState extends State<ProcessDetailPage> {
  final _formKey = GlobalKey<FormState>();
  TextEditingController nameController = TextEditingController(text: '');
  List<PhaseProcess> listPhase = [];

  TreePickerController treeController = TreePickerController();

  ProcessDetailCubit? _cubit;

  @override
  void initState() {
    super.initState();
    _cubit = BlocProvider.of<ProcessDetailCubit>(context);
    _cubit!.getProcessDetail(widget.process_id!);
  }

  Future<void> _refreshData() async {
    _cubit!.getProcessDetail(widget.process_id!);
  }

  @override
  void dispose() {
    _cubit!.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBarWidget(
        context: context,
        title: 'Chi tiết quy trình',
      ),
      body: _buildBody(context),
    );
  }

  Widget _buildBody(BuildContext context) {
    return SafeArea(
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
                      BlocConsumer<ProcessDetailCubit, ProcessDetailState>(
                        listener: (context, state) {
                          if (state.loadStatus == LoadStatus.SUCCESS) {
                            nameController =
                                TextEditingController(text: _cubit!.state.name);
                          }
                          // TODO: implement listener
                        },
                        builder: (context, state) {
                          return AppTextField(
                            autoValidateMode:
                                AutovalidateMode.onUserInteraction,
                            hintText: 'Nhập vào tên quy trình',
                            controller: nameController,
                            enable: false,
                          );
                        },
                      ),
                      SizedBox(height: 20),
                      Text(
                        'Các loại cây trồng áp dụng',
                        style: AppTextStyle.greyS14,
                      ),
                      SizedBox(height: 10),
                      BlocConsumer<ProcessDetailCubit, ProcessDetailState>(
                        listener: (context, state) {
                          if (state.loadStatus == LoadStatus.SUCCESS) {
                            treeController = TreePickerController(
                                treeList: _cubit!.state.trees);
                          }
                          // TODO: implement listener
                        },
                        builder: (context, state) => AppPageTreePicker(
                          controller: treeController,
                          onChanged: (value) {},
                          enabled: false,
                        ),
                      ),
                      SizedBox(height: 20),
                      Text(
                        'Các giai đoạn chăm sóc',
                        style: AppTextStyle.greyS14,
                      ),
                      SizedBox(height: 10),
                      BlocBuilder<ProcessDetailCubit, ProcessDetailState>(
                        builder: (context, state) {
                          if (state.loadStatus == LoadStatus.LOADING) {
                            return Center(
                                child: CircularProgressIndicator(
                              color: AppColors.main,
                            ));
                          } else if (state.loadStatus == LoadStatus.FAILURE) {
                            return Container();
                          } else if (state.loadStatus == LoadStatus.SUCCESS) {
                            return state.stages!.length != 0
                                ? Column(
                                    children: List.generate(
                                        state.stages!.length,
                                        (index) => PhaseProcess(
                                              index: index,
                                              cubitProcess: _cubit!,
                                              phase: '${index + 1}',
                                              onRemove: () {},
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
              SizedBox(height: 20),
              buildActionCreate(context),
            ],
          ),
        ),
      ),
    );
  }

  Widget buildActionCreate(BuildContext context) {
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
            title: 'Sửa',
            onPressed: () async {
              bool isUpdate = await Application.router!.navigateTo(
                appNavigatorKey.currentContext!,
                Routes.processUpdate,
                routeSettings: RouteSettings(
                  arguments: ProcessUpdateArgument(
                    process_id: widget.process_id,
                  ),
                ),
              );
              if (isUpdate) {
                _refreshData();
              }
            },
          ),
        ),
      ],
    );
  }
}

class PhaseProcess extends StatefulWidget {
  int? index;
  String? phase;
  VoidCallback? onRemove;
  ProcessDetailCubit cubitProcess;

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
          margin: EdgeInsets.only(left: 2, right: 2, bottom: 20),
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
                              BlocBuilder<ProcessDetailCubit,
                                  ProcessDetailState>(
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
                            ],
                          ),
                        ),
                      )
                    ],
                  )
                ]),
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
  final ProcessDetailCubit cubitProcess;

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
    return Container(
      height: 40,
      padding: EdgeInsets.all(10),
      margin: EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
          color: Color(0xFFDDDAEA),
          borderRadius: BorderRadius.all(Radius.circular(10))),
      child: Row(
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
    );
  }
}

class ProcessDetailArgument {
  String? process_id;

  ProcessDetailArgument({
    this.process_id,
  });
}

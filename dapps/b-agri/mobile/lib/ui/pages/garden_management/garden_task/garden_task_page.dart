import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/commons/screen_size.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/entities/garden_task/task_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/update_garden_task/update_garden_task_page.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_delete_dialog.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_emty_data_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/custome_slidable_widget.dart';
import 'package:flutter_base/ui/widgets/error_list_widget.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_html/shims/dart_ui.dart';
import 'package:flutter_slidable/flutter_slidable.dart';
import 'package:intl/intl.dart';

import 'add_garden_task/add_garden_task_page.dart';
import 'garden_task_cubit.dart';

class GardenTaskPage extends StatefulWidget {
  final String? garden_id;
  final String? name;
  final String? process_id;
  final String? season_id;

  GardenTaskPage(
      {Key? key, this.name, this.season_id, this.process_id, this.garden_id})
      : super(key: key);

  @override
  _GardenTaskPageState createState() => _GardenTaskPageState();
}

class _GardenTaskPageState extends State<GardenTaskPage> {
  GardenTaskCubit? _cubit;
  late TextEditingController dateController;

  @override
  void initState() {
    super.initState();
    _cubit = BlocProvider.of<GardenTaskCubit>(context);

    var now = new DateTime.now();
    var formatter = new DateFormat('dd-MM-yyyy');
    String formattedDate = formatter.format(now);
    _cubit!.getGardenTask(widget.season_id!, formattedDate);
    dateController = TextEditingController(text: formattedDate);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: widget.name!,
      ),
      floatingActionButton: AppFloatingActionButton(
        onPressed: () async {
          bool isAdd = await Application.router!.navigateTo(
            appNavigatorKey.currentContext!,
            Routes.taskCreate,
            routeSettings: RouteSettings(
              arguments: GardenTaskCreateArgument(
                name: widget.name,
                season_id: widget.season_id,
              ),
            ),
          );
          if (isAdd) {
            _onRefreshData();
          }
        },
      ),
      body: Padding(
        padding: EdgeInsets.only(top: 25, right: 10, left: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Text(
                'Danh sách công việc trong ngày:',
                style: AppTextStyle.tintS14,
              ),
            ),
            SizedBox(height: 15),
            BlocBuilder<GardenTaskCubit, GardenTaskState>(
              bloc: _cubit,
              buildWhen: (previous, current) =>
                  previous.taskStatus != current.taskStatus,
              builder: (context, state) {
                if (state.taskStatus == LoadStatus.LOADING) {
                  return Container(
                    height: ScreenSize.of(context).height / 2,
                    child: Center(
                        child: CircularProgressIndicator(
                      color: AppColors.main,
                    )),
                  );
                } else if (state.taskStatus == LoadStatus.FAILURE) {
                  return _buildFailureList();
                } else if (state.taskStatus == LoadStatus.SUCCESS) {
                  return state.taskList!.length != 0
                      ? Expanded(
                          child: RefreshIndicator(
                            onRefresh: _onRefreshData,
                            child: ListView.separated(
                              itemCount: state.taskList!.length,
                              padding: EdgeInsets.symmetric(vertical: 5),
                              shrinkWrap: true,
                              itemBuilder: (context, index) {
                                TaskEntity task = state.taskList![index];

                                return _buildItem(
                                    startTime: task.start_time,
                                    endTime: task.end_time,
                                    title: task.name,
                                    onUpdate: () async {
                                      bool isUpdate =
                                          await Application.router!.navigateTo(
                                        appNavigatorKey.currentContext!,
                                        Routes.taskUpdate,
                                        routeSettings: RouteSettings(
                                          arguments: GardenTaskUpdateArgument(
                                            name: widget.name,
                                            task_id: task.task_id,
                                            season_id: widget.season_id,
                                          ),
                                        ),
                                      );
                                      if (isUpdate) {
                                        _onRefreshData();
                                      }
                                    },
                                    onDelete: () async {
                                      bool isDelete = await showDialog(
                                          context: context,
                                          builder: (context) => AppDeleteDialog(
                                                onConfirm: () async {
                                                  final result = await _cubit!
                                                      .deleteTask(
                                                          task.task_id ?? "");
                                                  Navigator.pop(context, true);
                                                },
                                              ));

                                      if (isDelete) {
                                        _onRefreshData();
                                        showSnackBar(
                                            'Xóa công việc thành công!');
                                      }
                                    });
                              },
                              separatorBuilder: (context, index) =>
                                  SizedBox(height: 15),
                            ),
                          ),
                        )
                      : Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Center(
                                child: EmptyDataWidget(),
                              ),
                            ],
                          ),
                        );
                } else {
                  return Container();
                }
              },
            ),
          ],
        ),
      ),
    );
  }

  _buildItem(
      {String? startTime,
      String? endTime,
      String? title,
      VoidCallback? onPressed,
      VoidCallback? onUpdate,
      VoidCallback? onDelete}) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        decoration: BoxDecoration(
          color: AppColors.grayEC,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Slidable(
          groupTag: 'employeeTag',
          endActionPane: ActionPane(
            extentRatio: 1 / 3,
            motion: BehindMotion(),
            children: [
              CustomSlidableAction(
                  backgroundColor: AppColors.blueSlideButton,
                  foregroundColor: Colors.white,
                  onPressed: (BuildContext context) {
                    onUpdate?.call();
                  },
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SizedBox(
                        height: 20,
                        width: 20,
                        child: Image.asset(AppImages.icSlideEdit),
                      ),
                      SizedBox(height: 4),
                      FittedBox(
                        child: Text(
                          'Sửa',
                          style: AppTextStyle.whiteS16,
                        ),
                      )
                    ],
                  )),
              CustomSlidable(
                  backgroundColor: AppColors.redSlideButton,
                  foregroundColor: Colors.white,
                  onPressed: (BuildContext context) {
                    onDelete?.call();
                  },
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SizedBox(
                        height: 20,
                        width: 20,
                        child: Image.asset(AppImages.icSlideDelete),
                      ),
                      SizedBox(height: 4),
                      FittedBox(
                        child: Text(
                          'Xóa',
                          style: AppTextStyle.whiteS16,
                        ),
                      )
                    ],
                  )),
            ],
          ),
          child: Padding(
            padding:
                const EdgeInsets.only(top: 20, bottom: 20, left: 15, right: 15),
            child: Builder(builder: (thisContext) {
              SlidableController controller = Slidable.of(thisContext)!;
              return RowWidget(
                startTime: startTime,
                title: title,
                endTime: endTime,
                controller: controller,
              );
            }),
          ),
        ),
      ),
    );
  }

  Future<void> _onRefreshData() async {
    _cubit!.getGardenTask(widget.season_id!, dateController.text);
  }

  Widget _buildEmptyList() {
    return ErrorListWidget(
      text: S.of(context).no_data_show,
      onRefresh: _onRefreshData,
    );
  }

  Widget _buildFailureList() {
    return ErrorListWidget(
      text: S.of(context).error_occurred,
      onRefresh: _onRefreshData,
    );
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}

class RowWidget extends StatefulWidget {
  String? title;
  String? startTime;
  String? endTime;
  SlidableController controller;

  RowWidget({
    Key? key,
    this.title,
    this.endTime,
    this.startTime,
    required this.controller,
  }) : super(key: key);

  @override
  State<RowWidget> createState() => _RowWidgetState();
}

class _RowWidgetState extends State<RowWidget> {
  bool isOpen = true;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    widget.controller.actionPaneType.addListener(() {
      setState(() {
        isOpen = !isOpen;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(
          '${widget.startTime} - ${widget.endTime}:',
          style: AppTextStyle.blackS14,
        ),
        SizedBox(width: 7),
        Expanded(
            child: Text(
          '${widget.title}',
          overflow: TextOverflow.ellipsis,
          style: AppTextStyle.blackS14,
        )),
        // if (isOpen)
        //   Icon(
        //     Icons.arrow_forward_ios_rounded,
        //     color: Colors.grey,
        //     size: 20,
        //   )
      ],
    );
  }
}

class GardenTaskArgument {
  String? garden_id;
  String? name;
  String? season_id;
  String? process_id;

  GardenTaskArgument({
    this.garden_id,
    this.name,
    this.season_id,
    this.process_id,
  });
}

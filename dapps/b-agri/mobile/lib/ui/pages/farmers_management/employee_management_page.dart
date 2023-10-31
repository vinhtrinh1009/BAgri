import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/farmers_management/employee_management_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_error_list_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/custome_slidable_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_delete_dialog.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/drop_down_picker/app_manager_picker.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_html/shims/dart_ui.dart';
import 'package:flutter_slidable/flutter_slidable.dart';

class EmployeeManagementPage extends StatefulWidget {
  const EmployeeManagementPage({Key? key}) : super(key: key);

  @override
  _EmployeeManagementPageState createState() => _EmployeeManagementPageState();
}

class _EmployeeManagementPageState extends State<EmployeeManagementPage> {
  late EmployeeManagementCubit _employeeManagementCubit;
  late String managerId;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _employeeManagementCubit =
        BlocProvider.of<EmployeeManagementCubit>(context);
    _employeeManagementCubit.getListFarmer();
  }

  void refreshData() async {
    await _employeeManagementCubit.getListFarmer();
    _employeeManagementCubit.filterListFarmer(managerId);
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: AppFloatingActionButton(
        onPressed: () async {
          bool isAdd = await Application.router!.navigateTo(
            context,
            Routes.employeeAdding,
          );
          if (isAdd) {
            refreshData();
            showSnackBar('Thêm mới nhân công thành công!');
          }
        },
      ),
      appBar: AppBarWidget(
        title: 'Quản lý nhân công',
        context: context,
      ),
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 15),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 25),
              Text(
                'Người quản lý',
                style: AppTextStyle.greyS18,
              ),
              SizedBox(height: 8),
              AppCustomManagerPicker(
                managerId: "allManager",
                onChange: (value) {
                  setState(() {
                    managerId = value?.manager_id ?? "";
                  });
                  _employeeManagementCubit
                      .filterListFarmer(value?.manager_id ?? "");
                },
              ),
              SizedBox(height: 15),
              Expanded(
                  child: BlocBuilder<EmployeeManagementCubit,
                      EmployeeManagementState>(
                buildWhen: (prev, current) =>
                    prev.loadStatus != current.loadStatus ||
                    prev.currentFarmerList != current.currentFarmerList,
                builder: (context, state) {
                  if (state.loadStatus == LoadStatus.LOADING)
                    return Center(
                        child: CircularProgressIndicator(
                      color: AppColors.main,
                    ));
                  else if (state.loadStatus == LoadStatus.FAILURE)
                    return AppErrorListWidget(onRefresh: () async {
                      refreshData();
                    });
                  else if (state.loadStatus == LoadStatus.SUCCESS) {
                    return RefreshIndicator(
                      color: AppColors.main,
                      onRefresh: () async {
                        refreshData();
                      },
                      child: SlidableAutoCloseBehavior(
                        child: ListView.separated(
                            padding: EdgeInsets.symmetric(vertical: 5),
                            itemBuilder: (context, index) {
                              FarmerEntity farmer =
                                  state.currentFarmerList![index];
                              return _buildItem(
                                  name: farmer.fullName ?? "",
                                  onPressed: () {
                                    Application.router!.navigateTo(
                                        context, Routes.employeeDetail,
                                        routeSettings: RouteSettings(
                                            arguments: farmer.farmerId!));
                                  },
                                  onUpdate: () async {
                                    bool isUpdate = await Application.router!
                                        .navigateTo(
                                            context, Routes.employeeUpdating,
                                            routeSettings: RouteSettings(
                                                arguments: farmer.farmerId!));
                                    if (isUpdate) {
                                      refreshData();
                                      showSnackBar('Sửa nhân công thành công!');
                                    }
                                  },
                                  onDelete: () async {
                                    bool isDelete = await showDialog(
                                        context: context,
                                        builder: (context) => AppDeleteDialog(
                                              onConfirm: () async {
                                                await _employeeManagementCubit
                                                    .deleteFarmer(
                                                        farmer.farmerId ?? "");
                                                Navigator.pop(context, true);
                                              },
                                            ));

                                    if (isDelete) {
                                      refreshData();
                                      showSnackBar('Xóa nhân công thành công!');
                                    }
                                  });
                            },
                            separatorBuilder: (context, index) {
                              return SizedBox(height: 10);
                            },
                            itemCount: state.currentFarmerList?.length ?? 0),
                      ),
                    );
                  } else
                    return SizedBox();
                },
              ))
            ],
          ),
        ),
      ),
    );
  }

  _buildItem(
      {required String name,
      String? avatarUrl,
      VoidCallback? onDelete,
      VoidCallback? onPressed,
      VoidCallback? onUpdate}) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        height: 80,
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
                avatarUrl: avatarUrl,
                name: name,
                controller: controller,
              );
            }),
          ),
        ),
      ),
    );
  }
}

class RowWidget extends StatefulWidget {
  String? avatarUrl;
  String name;
  SlidableController controller;
  RowWidget({
    Key? key,
    this.avatarUrl,
    required this.name,
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
        Image.asset(widget.avatarUrl ?? AppImages.icEmployeeAvatar),
        SizedBox(width: 15),
        Expanded(
          child: Text(
            widget.name,
            style: AppTextStyle.greyS18Bold,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        SizedBox(width: 10),
        if (isOpen)
          Icon(
            Icons.arrow_forward_ios_rounded,
            color: Colors.grey,
            size: 20,
          )
      ],
    );
  }
}

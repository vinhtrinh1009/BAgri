import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/seasons_management/season_management_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_circular_progress_indicator.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_delete_dialog.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_error_list_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/custome_slidable_widget.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_slidable/flutter_slidable.dart';

class SeasonTabPage extends StatefulWidget {
  @override
  _SeasonTabPageState createState() => _SeasonTabPageState();
}

class _SeasonTabPageState extends State<SeasonTabPage>
    with SingleTickerProviderStateMixin {
  late TabController _controller;
  late SeasonManagementCubit _seasonManagementCubit;

  @override
  void initState() {
    super.initState();
    _seasonManagementCubit = BlocProvider.of<SeasonManagementCubit>(context);

    _controller = TabController(length: 2, vsync: this);
    _controller.addListener(() {
      setState(() {});
    });
  }

  @override
  void dispose() {
    super.dispose();
    _controller.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        title: 'Quản lý mùa vụ',
        context: context,
      ),
      body: Container(
          child: Padding(
        padding: const EdgeInsets.only(
          top: 9,
        ),
        child: Column(
          children: [
            Container(
              padding: EdgeInsets.symmetric(horizontal: 10),
              child: Row(
                children: [
                  Expanded(
                    child: TabItem(
                      controller: _controller,
                      title: 'Đang thực hiện',
                      index: 0,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TabItem(
                      controller: _controller,
                      title: 'Hoàn thành',
                      index: 1,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 9),
            Expanded(
              child: TabBarView(
                controller: _controller,
                children: [
                  SeasonManagementPage(status: ''),
                  SeasonManagementPage(
                    status: "done",
                  ),
                ],
              ),
            ),
          ],
        ),
      )),
    );
  }
}

class TabItem extends StatelessWidget {
  final TabController controller;
  final String title;
  final int index;

  TabItem({required this.controller, required this.title, required this.index});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        controller.animateTo(index);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(25),
          color:
              controller.index == index ? Color(0xFF4EC04B) : Color(0xFFECECEC),
        ),
        child: Align(
          alignment: Alignment.center,
          child: Text(
            title,
            style: controller.index == index
                ? const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFFFFFFFF))
                : const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF7A7A7A)),
          ),
        ),
      ),
    );
  }
}

class SeasonManagementPage extends StatefulWidget {
  String? status;
  SeasonManagementPage({Key? key, this.status}) : super(key: key);

  @override
  _SeasonManagementPageState createState() => _SeasonManagementPageState();
}

class _SeasonManagementPageState extends State<SeasonManagementPage> {
  late SeasonManagementCubit _seasonManagementCubit;

  @override
  void initState() {
    _seasonManagementCubit = BlocProvider.of<SeasonManagementCubit>(context);
    super.initState();

    refreshData();
  }

  @override
  void dispose() {
    super.dispose();
  }

  Future<void> refreshData() async {
    await _seasonManagementCubit.getListSeason(widget.status);
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
          bool isAdd = await Application.router!
              .navigateTo(context, Routes.seasonAdding);

          if (isAdd) {
            refreshData();
            showSnackBar('Thêm mới mùa vụ thành công!');
          }
        },
      ),
      body: SafeArea(
        child: BlocBuilder<SeasonManagementCubit, SeasonManagementState>(
          buildWhen: (prev, current) =>
              prev.loadStatus != current.loadStatus ||
              prev.seasonList != current.seasonList,
          builder: (context, state) {
            if (state.loadStatus == LoadStatus.LOADING) {
              return Center(
                child: AppCircularProgressIndicator(),
              );
            } else if (state.loadStatus == LoadStatus.FAILURE) {
              return AppErrorListWidget(onRefresh: () async {
                refreshData();
              });
            } else if (state.loadStatus == LoadStatus.SUCCESS) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                      child: RefreshIndicator(
                    color: AppColors.main,
                    onRefresh: () async {
                      refreshData();
                    },
                    child: ListView.separated(
                        padding:
                            EdgeInsets.symmetric(horizontal: 15, vertical: 10),
                        itemBuilder: (context, index) {
                          SeasonEntity season = state.seasonList![index];
                          return _buildItem(
                              gardenName: season.garden?.name ?? "",
                              seasonName: season.name ?? "",
                              processName: season.process?.name ?? "",
                              onPressed: () {
                                Application.router!.navigateTo(
                                    context, Routes.seasonDetail,
                                    routeSettings:
                                        RouteSettings(arguments: season));
                              },
                              onUpdate: () async {
                                bool isUpdate = await Application.router!
                                    .navigateTo(context, Routes.seasonUpdating,
                                        routeSettings: RouteSettings(
                                            arguments: season.seasonId!));
                                if (isUpdate) {
                                  refreshData();
                                  showSnackBar('Sửa mùa vụ thành công!');
                                }
                              },
                              onDelete: () async {
                                bool isDelete = await showDialog(
                                    context: context,
                                    builder: (context) => AppDeleteDialog(
                                          onConfirm: () async {
                                            final result =
                                                await _seasonManagementCubit
                                                    .deleteSeason(
                                                        season.seasonId ?? "");
                                            // if (result) {
                                            //   Navigator.pop(context, true);
                                            // } else {
                                            //   Navigator.pop(context, false);
                                            // }
                                            Navigator.pop(context, true);
                                          },
                                        ));

                                if (isDelete) {
                                  refreshData();
                                  showSnackBar('Xóa mùa vụ thành công!');
                                }
                              });
                        },
                        separatorBuilder: (context, index) {
                          return SizedBox(height: 10);
                        },
                        itemCount: state.seasonList?.length ?? 0),
                  ))
                ],
              );
            } else
              return SizedBox();
          },
        ),
      ),
    );
  }

  _buildItem(
      {required String gardenName,
      required String seasonName,
      required String processName,
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
          endActionPane: widget.status != "done"
              ? ActionPane(
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
                )
              : null,
          child: Padding(
            padding:
                const EdgeInsets.only(top: 20, bottom: 20, left: 15, right: 15),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '$gardenName - $seasonName',
                        style: AppTextStyle.greyS16Bold,
                        overflow: TextOverflow.ellipsis,
                      ),
                      SizedBox(height: 5),
                      Text(
                        'Quy trình: $processName',
                        style: AppTextStyle.greyS14,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
                Icon(
                  Icons.arrow_forward_ios_rounded,
                  color: Colors.grey,
                  size: 20,
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}

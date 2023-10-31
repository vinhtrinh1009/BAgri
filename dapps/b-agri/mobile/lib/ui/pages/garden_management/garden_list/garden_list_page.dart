import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';

import 'package:flutter_base/models/entities/garden/season_entity.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';

import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/auth/login/login_cubit.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_detail/garden_detail.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_update/garden_update.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_delete_dialog.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_emty_data_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_error_list_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/custome_slidable_widget.dart';

import 'package:flutter_base/ui/widgets/error_list_widget.dart';
import 'package:flutter_base/utils/dialog_utils.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_slidable/flutter_slidable.dart';

import 'garden_list_cubit.dart';

class GardenListPage extends StatefulWidget {
  @override
  _GardenListState createState() => _GardenListState();
}

class _GardenListState extends State<GardenListPage> {
  GardenListCubit? _cubit;

  final _scrollController = ScrollController();
  final _scrollThreshold = 200.0;

  @override
  void initState() {
    super.initState();
    _cubit = BlocProvider.of<GardenListCubit>(context);
    _cubit!.fetchGardenList();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    super.dispose();
    _scrollController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        title: "Quản lý vườn",
        context: context,
      ),
      body: Container(
        child: BlocBuilder<GardenListCubit, GardenListState>(
          bloc: _cubit,
          buildWhen: (previous, current) =>
              previous.getGardenStatus != current.getGardenStatus,
          builder: (context, state) {
            if (state.getGardenStatus == LoginStatusBagri.LOADING) {
              return Center(
                  child: CircularProgressIndicator(
                color: AppColors.main,
              ));
            } else if (state.getGardenStatus == LoginStatusBagri.FAILURE) {
              return AppErrorListWidget(
                onRefresh: _onRefreshData,
              );
            } else if (state.getGardenStatus == LoginStatusBagri.SUCCESS) {
              return state.listGardenData!.length != 0
                  ? RefreshIndicator(
                      color: AppColors.main,
                      onRefresh: _onRefreshData,
                      child: ListView.separated(
                        padding: EdgeInsets.only(
                            left: 10, right: 10, top: 10, bottom: 25),
                        physics: AlwaysScrollableScrollPhysics(),
                        itemCount: state.listGardenData!.length,
                        shrinkWrap: true,
                        primary: false,
                        controller: _scrollController,
                        itemBuilder: (context, index) {
                          GardenEntity garden = state.listGardenData![index];
                          return _buildItem(
                              gardenName: garden.name ?? "",
                              gardenId: garden.garden_id ?? "",
                              area: garden.area,
                              process: garden.process,
                              season: garden.season,
                              onPressed: () {
                                Application.router!.navigateTo(
                                  appNavigatorKey.currentContext!,
                                  Routes.gardenDetail,
                                  routeSettings: RouteSettings(
                                    arguments: GardenArgument(
                                      titleScreen: garden.name,
                                      garden_id: garden.garden_id,
                                    ),
                                  ),
                                );
                              },
                              onUpdate: () async {
                                bool isUpdate =
                                    await Application.router!.navigateTo(
                                  appNavigatorKey.currentContext!,
                                  Routes.gardenUpdate,
                                  routeSettings: RouteSettings(
                                    arguments: GardenUpdateArgument(
                                      garden_id: garden.garden_id,
                                      name: garden.name,
                                      area: garden.area,
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
                                            await _cubit!
                                                .deleteGarden(garden.garden_id);
                                            Navigator.pop(context, true);
                                          },
                                        ));

                                if (isDelete) {
                                  _onRefreshData();
                                  showSnackBar('Xóa vườn thành công!');
                                }
                              });
                        },
                        separatorBuilder: (context, index) {
                          return SizedBox(height: 10);
                        },
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
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          bool isAdd = await Application.router
              ?.navigateTo(context, Routes.gardenCreate);
          if (isAdd) {
            _onRefreshData();
          }
        },
        backgroundColor: AppColors.main,
        child: Icon(
          Icons.add,
          size: 40,
        ),
      ),
    );
  }

  _buildItem(
      {required String gardenName,
      required String gardenId,
      int? area,
      ProcessEntity? process,
      SeasonEntity? season,
      VoidCallback? onDelete,
      VoidCallback? onPressed,
      VoidCallback? onUpdate}) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        height: 60,
        decoration: BoxDecoration(
          color: AppColors.grayEC,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Slidable(
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
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    '$gardenName',
                    style: AppTextStyle.greyS16Bold,
                    overflow: TextOverflow.ellipsis,
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

  Future<void> _onRefreshData() async {
    _cubit!.fetchGardenList();
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }

  void _onScroll() {
    final maxScroll = _scrollController.position.maxScrollExtent;
    final currentScroll = _scrollController.position.pixels;
    if (maxScroll - currentScroll <= _scrollThreshold) {
      // _cubit!.fetchNextGardenData();
    }
  }

  @override
  bool get wantKeepAlive => true;
}

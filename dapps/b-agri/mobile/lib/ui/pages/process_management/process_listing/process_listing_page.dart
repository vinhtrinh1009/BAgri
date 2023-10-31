import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/process_management/process_detail/process_detail_page.dart';
import 'package:flutter_base/ui/pages/process_management/process_listing/process_listing_cubit.dart';
import 'package:flutter_base/ui/pages/process_management/update_process/update_process_page.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_delete_dialog.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_emty_data_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_error_list_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_base/ui/widgets/b_agri/custome_slidable_widget.dart';
import 'package:flutter_base/ui/widgets/error_list_widget.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_slidable/flutter_slidable.dart';

class TabListProcess extends StatelessWidget {
  const TabListProcess({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) {
        final processRepository =
            RepositoryProvider.of<ProcessRepository>(context);
        return ProcessListCubit(processRepository: processRepository);
      },
      child: ProcessListPage(),
    );
  }
}

class ProcessListPage extends StatefulWidget {
  @override
  _ProcessListPageState createState() => _ProcessListPageState();
}

class _ProcessListPageState extends State<ProcessListPage>
    with AutomaticKeepAliveClientMixin {
  ProcessListCubit? _cubit;
  final _scrollController = ScrollController();
  final _scrollThreshold = 200.0;

  @override
  void initState() {
    super.initState();
    _cubit = BlocProvider.of<ProcessListCubit>(context);
    _cubit!.fetchListProcess();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        resizeToAvoidBottomInset: false,
        backgroundColor: Colors.white,
        body: _buildBody(),
        floatingActionButton: FloatingActionButton(
          heroTag: "btn1",
          onPressed: () async {
            bool? isAdd = await Application.router
                ?.navigateTo(context, Routes.processCreate);
            if (isAdd == true) {
              _onRefreshData();
            }
          },
          backgroundColor: AppColors.main,
          child: Icon(
            Icons.add,
            size: 40,
          ),
        ),
      ),
    );
  }

  Widget _buildBody() {
    return BlocBuilder<ProcessListCubit, ProcessListState>(
      bloc: _cubit,
      buildWhen: (previous, current) =>
          previous.getProcessStatus != current.getProcessStatus,
      builder: (context, state) {
        if (state.getProcessStatus == LoadStatus.LOADING) {
          return Center(
              child: CircularProgressIndicator(
            color: AppColors.main,
          ));
        } else if (state.getProcessStatus == LoadStatus.FAILURE) {
          return AppErrorListWidget(onRefresh: _onRefreshData);
        } else if (state.getProcessStatus == LoadStatus.SUCCESS) {
          return state.listData!.length != 0
              ? RefreshIndicator(
                  color: AppColors.main,
                  onRefresh: _onRefreshData,
                  child: SlidableAutoCloseBehavior(
                    child: ListView.separated(
                      padding: EdgeInsets.only(
                          left: 10, right: 10, top: 10, bottom: 25),
                      physics: AlwaysScrollableScrollPhysics(),
                      itemCount: state.listData!.length,
                      shrinkWrap: true,
                      primary: false,
                      controller: _scrollController,
                      separatorBuilder: (context, index) =>
                          SizedBox(height: 10),
                      itemBuilder: (context, index) {
                        ProcessEntity process = state.listData![index];
                        return _buildItem(
                            processName: process.name ?? "",
                            processId: process.process_id ?? "",
                            trees: process.trees ?? [],
                            onPressed: () {
                              Application.router!.navigateTo(
                                appNavigatorKey.currentContext!,
                                Routes.processDetail,
                                routeSettings: RouteSettings(
                                  arguments: ProcessDetailArgument(
                                    process_id: process.process_id,
                                  ),
                                ),
                              );
                            },
                            onUpdate: () async {
                              bool isUpdate =
                                  await Application.router!.navigateTo(
                                appNavigatorKey.currentContext!,
                                Routes.processUpdate,
                                routeSettings: RouteSettings(
                                  arguments: ProcessUpdateArgument(
                                    process_id: process.process_id,
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
                                              .deleteProcess(
                                                  process.process_id);
                                          Navigator.pop(context, true);
                                        },
                                      ));

                              if (isDelete) {
                                _onRefreshData();
                                showSnackBar('Xóa quy trình thành công!');
                              }
                            });
                      },
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
    );
  }

  Widget _buildItem(
      {required String processName,
      required String processId,
      required List<TreeEntity> trees,
      VoidCallback? onDelete,
      VoidCallback? onPressed,
      VoidCallback? onUpdate}) {
    String treeString = "";

    for (int i = 0; i < trees.length; i++) {
      if (i == trees.length - 1) {
        treeString += '${trees[i].name ?? ""}';
      } else {
        treeString += '${trees[i].name ?? ""}, ';
      }
    }
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        height: 80,
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
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '$processName',
                        style: AppTextStyle.greyS16Bold,
                        overflow: TextOverflow.ellipsis,
                      ),
                      SizedBox(height: 5),
                      Text(
                        'Loại cây trồng: $treeString',
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
    _cubit!.fetchListProcess();
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

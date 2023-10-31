import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:flutter_base/models/entities/process/stage_entity.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/process_management/process_season/process_season_page.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/season_detail_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/widgets/care_process_detail.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/widgets/generate_qrcode.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_circular_progress_indicator.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_confirmed_dialog.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_error_list_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_snackbar.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_base/utils/date_utils.dart' as Util;

final careProcessNavigationKey = GlobalKey<NavigatorState>();

class SeasonDetailPage extends StatefulWidget {
  SeasonEntity thisSeason;

  SeasonDetailPage({Key? key, required this.thisSeason}) : super(key: key);

  @override
  _SeasonDetailPageState createState() => _SeasonDetailPageState();
}

class _SeasonDetailPageState extends State<SeasonDetailPage> {
  late SeasonDetailCubit _cubit;

  @override
  void initState() {
    _cubit = BlocProvider.of<SeasonDetailCubit>(context);
    super.initState();
    _cubit.getSeasonDetail(widget.thisSeason.seasonId ?? "");
  }

  Future<void> refreshData() async {
    _cubit.getSeasonDetail(widget.thisSeason.seasonId ?? "");
  }

  String currentDayInProcess(String startDay) {
    DateTime startDateTime =
        Util.DateUtils.fromStringFormatStrikeThrough(startDay)!;
    Duration different = DateTime.now().difference(startDateTime);
    different = different + Duration(days: 1);
    return "${different.inDays}";
  }

  String currentStageInProcess(ProcessEntity process) {
    int currentStage = 0;
    if (process.stages != null) {
      stageLoop:
      for (int i = 0; i < process.stages!.length; i++) {
        StageEntity thisStage = process.stages![i];
        if (thisStage.steps != null) {
          stepLoop:
          for (int j = 0; j < thisStage.steps!.length; j++) {
            StepEntity thisStep = thisStage.steps![j];
            if (thisStep.actual_day != null) {
              currentStage = i;
              continue;
            } else {
              break stageLoop;
            }
          }
        }
      }
    }
    currentStage += 1;
    return '$currentStage';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title:
            "${widget.thisSeason.garden?.name ?? ""} - ${widget.thisSeason.name ?? ""}",
        rightActions: [
          BlocBuilder<SeasonDetailCubit, SeasonDetailState>(
            builder: (context, state) {
              if (state.season?.status != 'done') {
                return SizedBox();
              }
              return AppButton(
                color: AppColors.main,
                height: 40,
                child: SizedBox(
                    height: 20,
                    width: 20,
                    child: Image.asset(
                      AppImages.icQRCode,
                      fit: BoxFit.fill,
                    )),
                onPressed: () async {
                  bool isConfirmed =
                      await _cubit.generateQRCode(state.season?.seasonId ?? "");
                  if (isConfirmed) {
                    showDialog(
                        context: context,
                        builder: (BuildContext context) => BlocProvider.value(
                              value: _cubit,
                              child: QRCodeWidget(
                                data: state.season!.seasonId!,
                                nameSeason: state.season!.name!,
                                linkQR: state.linkQR,
                                linkUrl: state.linkUrl,
                              ),
                            ));
                  } else {
                    showSnackBar('Có lỗi xảy ra');
                  }
                },
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: BlocBuilder<SeasonDetailCubit, SeasonDetailState>(
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
                  RefreshIndicator(
                    color: AppColors.main,
                    onRefresh: () async {
                      refreshData();
                    },
                    child: SingleChildScrollView(
                      physics: AlwaysScrollableScrollPhysics(),
                      child: Padding(
                        padding: EdgeInsets.symmetric(horizontal: 15),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            SizedBox(height: 15),
                            Text(
                              'Thông tin chi tiết:',
                              style: AppTextStyle.blackS18Bold,
                            ),
                            SizedBox(height: 5),
                            Text(
                              'Loại cây trồng: ${state.season?.tree?.name ?? ""}',
                              style: AppTextStyle.greyS16,
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Quy trình: ${state.season?.process?.name ?? ""}',
                              style: AppTextStyle.greyS16,
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Ngày chăm sóc: ${currentDayInProcess(state.season!.start_date!)}',
                              style: AppTextStyle.greyS16,
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Giai đoạn ${currentStageInProcess(state.season!.process!)}',
                              style: AppTextStyle.greyS16,
                            ),
                            SizedBox(height: 20),
                            Text(
                              'Quá trình chăm sóc:',
                              style: AppTextStyle.blackS18Bold,
                            ),
                            SizedBox(height: 4),
                            Row(
                              children: [
                                Flexible(
                                  child: Text(
                                    'Quy trình áp dụng: ${state.season?.process?.name}',
                                    style: AppTextStyle.blackS18,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                                SizedBox(width: 10),
                                (state.season!.status == "done")
                                    ? SizedBox()
                                    : GestureDetector(
                                        onTap: () async {
                                          bool isUpdate = await Application
                                              .router!
                                              .navigateTo(
                                            appNavigatorKey.currentContext!,
                                            Routes.processSeasonUpdate,
                                            routeSettings: RouteSettings(
                                              arguments: ProcessSeasonArgument(
                                                process_id: state.season
                                                    ?.process?.process_id,
                                              ),
                                            ),
                                          );
                                          if (isUpdate) {
                                            refreshData();
                                          }
                                        },
                                        child: SizedBox(
                                          height: 20,
                                          width: 20,
                                          child: Image.asset(
                                            AppImages.icSlideEdit,
                                            color: AppColors.blue5B,
                                          ),
                                        ),
                                      ),
                              ],
                            ),
                            SizedBox(height: 20),
                          ],
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    child: Navigator(
                      key: careProcessNavigationKey,
                      initialRoute: '/',
                      onGenerateRoute: (RouteSettings settings) {
                        late Widget page;
                        switch (settings.name) {
                          case "/":
                            page = CareProcessDetail(
                              seasonId: widget.thisSeason.seasonId!,
                            );

                            break;
                        }
                        return MaterialPageRoute<dynamic>(
                          builder: (context) {
                            return page;
                          },
                          settings: settings,
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      (state.season!.status == "done")
                          ? SizedBox()
                          : AppButton(
                              color: Color(0xFF01A560),
                              title: 'Kết thúc mùa vụ',
                              height: 40,
                              width: 200,
                              onPressed: () async {
                                bool isConfirmed = await showDialog(
                                    context: context,
                                    builder: (context) => AppConfirmedDialog(
                                          onConfirm: () async {
                                            final result =
                                                await _cubit.updateSeason(
                                                    state.season?.seasonId ??
                                                        "");
                                            if (result != false) {
                                              final resultQR =
                                                  await _cubit.generateQRCode(
                                                      state.season?.seasonId ??
                                                          "");
                                              if (resultQR != false) {
                                                Navigator.pop(context, true);
                                                refreshData();
                                              } else {
                                                Navigator.pop(context, false);
                                              }
                                            } else {
                                              Navigator.pop(context, false);
                                            }
                                          },
                                        ));

                                if (isConfirmed) {
                                  showDialog(
                                      context: context,
                                      builder: (BuildContext context) =>
                                          BlocProvider.value(
                                            value: _cubit,
                                            child: QRCodeWidget(
                                              data: state.season!.seasonId!,
                                              nameSeason: state.season!.name!,
                                              linkQR: state.linkQR,
                                              linkUrl: state.linkUrl,
                                            ),
                                          ));
                                } else {
                                  showSnackBar('Có lỗi xảy ra');
                                }
                              },
                            ),
                    ],
                  ),
                  SizedBox(
                    height: 20,
                  ),
                ],
              );
            } else
              return SizedBox();
          },
        ),
      ),
    );
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(AppSnackBar(
      message: message,
    ));
  }
}

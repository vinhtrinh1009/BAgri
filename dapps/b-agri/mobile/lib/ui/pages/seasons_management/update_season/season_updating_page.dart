import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/seasons_management/add_season/season_adding_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/update_season/season_updating_cubit.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_dropdown_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/garden_picker/app_garden_picker.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/process_picker/app_process_picker.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/tree_picker/app_single_tree_picker.dart';
import 'package:flutter_base/utils/date_utils.dart' as Util;
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:screenshot/screenshot.dart';

class SeasonUpdatingPage extends StatefulWidget {
  String seasonId;

  SeasonUpdatingPage({Key? key, required this.seasonId}) : super(key: key);

  @override
  _SeasonUpdatingPageState createState() => _SeasonUpdatingPageState();
}

class _SeasonUpdatingPageState extends State<SeasonUpdatingPage> {
  late SeasonUpdatingCubit _cubit;
  late TextEditingController nameController;

  late SingleTreePickerController treeController;
  late ProcessPickerController processController;
  late GardenPickerController gardenController;

  @override
  void initState() {
    _cubit = BlocProvider.of<SeasonUpdatingCubit>(context);
    nameController = TextEditingController();
    treeController = SingleTreePickerController();
    processController = ProcessPickerController();
    gardenController = GardenPickerController();
    super.initState();
    _cubit.getSeasonDetail(widget.seasonId);

    nameController.addListener(() {
      _cubit.changeSeasonName(nameController.text);
    });
    treeController.addListener(() {
      _cubit.changeTree(treeController.treeEntity!);
      processController.processEntity = null;
    });
    gardenController.addListener(() {
      _cubit.changeGarden(gardenController.gardenEntity!);
    });
    processController.addListener(() {
      _cubit.changeProcess(processController.processEntity);
      if (processController.processEntity != null) {
        _cubit
            .changeDuration(processController.processEntity!.process_id ?? "");
      }
    });
  }

  @override
  void dispose() {
    super.dispose();
    nameController.dispose();
    gardenController.dispose();
    processController.dispose();
    treeController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Sửa mùa vụ',
      ),
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 15, vertical: 15),
          child: SingleChildScrollView(
            child: BlocConsumer<SeasonUpdatingCubit, SeasonUpdatingState>(
              listenWhen: (prev, current) =>
                  prev.seasonDetail != current.seasonDetail,
              listener: (context, state) {
                nameController.text = state.seasonName ?? "";
                treeController.treeEntity = state.treeEntity;
                gardenController.gardenEntity = state.gardenEntity;

                ///set Tree first then set process => change endTime because of process change=>duration change => endTime change
                processController.processEntity = state.processEntity;
              },
              builder: (context, state) {
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Tên mùa vụ',
                      style: AppTextStyle.greyS18,
                    ),
                    SizedBox(height: 10),
                    AppTextField(
                      controller: nameController,
                      hintText: 'Nhập vào tên mùa vụ',
                      enable:
                          state.loadStatus == LoadStatus.LOADING ? false : true,
                    ),
                    SizedBox(height: 20),
                    Text(
                      'Chọn vườn',
                      style: AppTextStyle.greyS18,
                    ),
                    SizedBox(height: 10),
                    AppPageGardenPicker(
                      controller: gardenController,
                      onChanged: (value) {},
                    ),
                    SizedBox(height: 20),
                    Text(
                      'Chọn loại cây',
                      style: AppTextStyle.greyS18,
                    ),
                    SizedBox(height: 10),
                    AppPageSingleTreePicker(
                      controller: treeController,
                      onChanged: (value) {},
                    ),
                    SizedBox(height: 20),
                    Text(
                      'Chọn quy trình chăm sóc',
                      style: AppTextStyle.greyS18,
                    ),
                    SizedBox(height: 10),
                    BlocBuilder<SeasonUpdatingCubit, SeasonUpdatingState>(
                      buildWhen: (prev, current) =>
                          prev.treeEntity != current.treeEntity ||
                          prev.processEntity != current.processEntity,
                      builder: (context, state) {
                        return AppPageProcessPicker(
                          enabled: false,
                          controller: processController,
                          treeId: state.treeEntity?.tree_id ?? null,
                          onChanged: (value) {},
                        );
                      },
                    ),
                    SizedBox(
                      height: 20,
                    ),
                    BlocBuilder<SeasonUpdatingCubit, SeasonUpdatingState>(
                      buildWhen: (prev, current) =>
                          prev.startTime != current.startTime ||
                          prev.endTime != current.endTime,
                      builder: (context, state) {
                        return Column(
                          children: [
                            Row(
                              children: [
                                Flexible(
                                  child: Text(
                                    'Ngày bắt đầu:',
                                    style: AppTextStyle.greyS18,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                                SizedBox(width: 15),
                                Text(
                                  state.startTime ?? "dd/mm/yyyy",
                                  style: AppTextStyle.blackS16.copyWith(
                                      decoration: TextDecoration.underline),
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                GestureDetector(
                                  onTap: state.loadStatus == LoadStatus.LOADING
                                      ? null
                                      : () async {
                                          final result = await showDatePicker(
                                              context: context,
                                              locale: Locale('vi'),
                                              initialEntryMode:
                                                  DatePickerEntryMode.input,
                                              builder: (context, child) {
                                                return _buildCalendarTheme(
                                                    child);
                                              },
                                              fieldHintText: 'dd/mm/yyyy',
                                              initialDate: state.startTime !=
                                                      null
                                                  ? Util.DateUtils.fromString(
                                                      state.startTime!,
                                                      format: AppConfig
                                                          .dateDisplayFormat)!
                                                  : DateTime.now(),
                                              firstDate: DateTime(2000),
                                              lastDate: DateTime(2024));
                                          if (result != null) {
                                            _cubit.changeStartTime(
                                              Util.DateUtils.toDateString(
                                                  result),
                                            );
                                          }
                                        },
                                  child: SizedBox(
                                    height: 26,
                                    width: 26,
                                    child: Image.asset(
                                      AppImages.icCalendar,
                                      fit: BoxFit.fill,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 15),
                            Row(
                              children: [
                                Flexible(
                                  child: Text(
                                    'Ngày kết thúc (dự kiến):',
                                    style: AppTextStyle.greyS18,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                                SizedBox(width: 15),
                                Text(
                                  state.endTime ?? "dd/mm/yyyy",
                                  style: AppTextStyle.blackS16.copyWith(
                                      decoration: TextDecoration.underline),
                                ),
                              ],
                            ),
                          ],
                        );
                      },
                    ),
                    SizedBox(height: 30),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Expanded(
                          child: AppButton(
                            color: AppColors.redButton,
                            title: 'Hủy bỏ',
                            onPressed: () {
                              Navigator.of(context).pop(false);
                            },
                          ),
                        ),
                        SizedBox(width: 25),
                        BlocBuilder<SeasonUpdatingCubit, SeasonUpdatingState>(
                          builder: (context, state) {
                            return Expanded(
                              child: AppButton(
                                color: AppColors.main,
                                isEnabled: state.buttonEnabled,
                                isLoading:
                                    state.loadStatus == LoadStatus.LOADING
                                        ? true
                                        : false,
                                title: 'Xác nhận',
                                onPressed: () async {
                                  await _cubit.updateSeason(widget.seasonId);
                                  Navigator.of(context).pop(true);
                                },
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                    SizedBox(height: 10),
                  ],
                );
              },
            ),
          ),
        ),
      ),
    );
  }

  Theme _buildCalendarTheme(Widget? child) {
    return Theme(
      data: ThemeData.light().copyWith(
        colorScheme: ColorScheme.light(
            primary: AppColors.main,
            surface: AppColors.main,
            // onSurface: AppColors.main,
            background: AppColors.main,
            onPrimary: Colors.white),
      ),
      child: child!,
    );
  }
}

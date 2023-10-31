import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/repositories/season_repository.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/season_step/season_step_cubit.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'app_step_picker_page.dart';

class StepPickerController extends ValueNotifier<StepEntity?> {
  StepPickerController({StepEntity? stepEntity}) : super(stepEntity);

  StepEntity? get stepEntity => value;

  set stepEntity(StepEntity? stepEntity) {
    value = stepEntity;
    notifyListeners();
  }
}

class AppPageStepPicker extends StatelessWidget {
  final StepPickerController controller;
  final ValueChanged<StepEntity?>? onChanged;
  final String seasonId;
  final bool enabled;

  AppPageStepPicker({
    required this.seasonId,
    required this.controller,
    this.onChanged,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: controller,
      builder: (context, StepEntity? stepEntity, child) {
        String text = "";

        if (stepEntity != null) {
          text += stepEntity.name ?? "";
        }
        return GestureDetector(
          onTap: enabled
              ? () {
                  _showMyProjectPicker(context: context);
                }
              : null,
          child: Stack(
            children: [
              Container(
                height: 48,
                decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(10)),
              ),
              TextFormField(
                enabled: false,
                controller: TextEditingController(text: text),
                decoration: InputDecoration(
                  hintText: 'Chọn bước',
                  suffixIcon: Padding(
                      padding: const EdgeInsets.only(right: 10),
                      child: Icon(Icons.keyboard_arrow_down)),
                  suffixIconConstraints:
                      BoxConstraints(maxHeight: 32, maxWidth: 32),
                  contentPadding: const EdgeInsets.only(
                    left: 20,
                    right: 15,
                    top: 10,
                    bottom: 10,
                  ),
                  errorBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                    borderSide: BorderSide(color: AppColors.redTextButton),
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                    borderSide: BorderSide(color: AppColors.lineGray),
                  ),
                  disabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: AppColors.main),
                      borderRadius: BorderRadius.circular(10)),
                  enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: AppColors.main),
                      borderRadius: BorderRadius.circular(10)),
                  focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: AppColors.main),
                      borderRadius: BorderRadius.circular(10)),
                  // focusedErrorBorder: OutlineInputBorder(
                  //   // borderRadius: BorderRadius.circular(10),
                  //   borderSide: BorderSide(color: AppColors.lineGray),
                  // ),
                  hintStyle: AppTextStyle.greyS14,
                ),
                style: AppTextStyle.blackS16,
              ),
            ],
          ),
        );
      },
    );
  }

  _showMyProjectPicker({
    required BuildContext context,
  }) async {
    final result = await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) {
          return BlocProvider(
            create: (context) {
              final seasonRepository =
                  RepositoryProvider.of<SeasonRepository>(context);
              return SeasonStepCubit(seasonRepository: seasonRepository);
            },
            child: AppStepPickerPage(
              seasonId: seasonId,
              selectedStepId: controller.stepEntity?.step_id ?? "",
            ),
          );
        },
      ),
    );
    if (result is StepEntity) {
      controller.stepEntity = result;
      onChanged?.call(result);
    }
  }
}

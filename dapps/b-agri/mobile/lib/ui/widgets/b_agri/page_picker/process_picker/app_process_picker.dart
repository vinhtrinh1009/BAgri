import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';

import 'package:flutter_base/models/entities/tree/list_tree_response.dart';

import 'app_process_picker_page.dart';

class ProcessPickerController extends ValueNotifier<ProcessEntity?> {
  ProcessPickerController({ProcessEntity? processEntity})
      : super(processEntity);

  ProcessEntity? get processEntity => value;

  set processEntity(ProcessEntity? processValue) {
    value = processValue;

    notifyListeners();
  }
}

class AppPageProcessPicker extends StatelessWidget {
  final ProcessPickerController controller;
  final ValueChanged<ProcessEntity?>? onChanged;
  final String? treeId;
  final bool enabled;

  AppPageProcessPicker({
    required this.controller,
    this.onChanged,
    this.treeId,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: controller,
      builder: (context, ProcessEntity? processEntity, child) {
        String text = processEntity?.name ?? "";

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
                  hintText: 'Chọn quy trình chăm sóc',
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
          return AppProcessPickerPage(
            selectedProcessId: controller.processEntity?.process_id ?? "",
            selectedTreeId: treeId,
          );
        },
      ),
    );
    if (result is ProcessEntity) {
      controller.processEntity = result;
      onChanged?.call(result);
    }
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

import 'package:flutter_base/models/entities/tree/list_tree_response.dart';

import 'app_single_tree_picker_page.dart';

class SingleTreePickerController extends ValueNotifier<TreeEntity?> {
  SingleTreePickerController({TreeEntity? treeEntity}) : super(treeEntity);

  TreeEntity? get treeEntity => value;

  set treeEntity(TreeEntity? treeValue) {
    value = treeValue;
    notifyListeners();
  }
}

class AppPageSingleTreePicker extends StatelessWidget {
  final SingleTreePickerController controller;
  final ValueChanged<TreeEntity?>? onChanged;

  final bool enabled;

  AppPageSingleTreePicker({
    required this.controller,
    this.onChanged,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: controller,
      builder: (context, TreeEntity? treeEntity, child) {
        String text = "";

        if (treeEntity != null) {
          text += treeEntity.name ?? "";
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
                  hintText: 'Chọn loại cây',
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
          return AppSingleTreePickerPage(
            selectedTreeId: controller.treeEntity?.tree_id ?? "",
          );
        },
      ),
    );
    if (result is TreeEntity) {
      controller.treeEntity = result;
      onChanged?.call(result);
    }
  }
}

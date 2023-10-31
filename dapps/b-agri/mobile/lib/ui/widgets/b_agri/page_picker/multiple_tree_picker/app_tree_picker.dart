import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

import 'package:flutter_base/models/entities/tree/list_tree_response.dart';

import 'app_tree_picker_page.dart';

class TreePickerController extends ValueNotifier<List<TreeEntity>?> {
  TreePickerController({List<TreeEntity>? treeList}) : super(treeList);

  List<TreeEntity>? get treeList => value;

  set tree(List<TreeEntity>? treeList) {
    value = treeList;
    notifyListeners();
  }
}

class AppPageTreePicker extends StatelessWidget {
  final TreePickerController controller;
  final ValueChanged<List<TreeEntity>?>? onChanged;

  final bool enabled;

  AppPageTreePicker({
    required this.controller,
    this.onChanged,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: controller,
      builder: (context, List<TreeEntity>? treeList, child) {
        String text = "";

        if (treeList != null) {
          for (int i = 0; i < treeList.length; i++) {
            if (i == treeList.length - 1) {
              text += '${treeList[i].name!}';
            } else {
              text += '${treeList[i].name!}, ';
            }
          }
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
                style: AppTextStyle.blackS14,
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
          List<String> list = [];
          if (controller.treeList != null) {
            for (TreeEntity e in controller.treeList!) {
              list.add(e.tree_id!);
            }
          }
          return AppTreePickerPage(
            selectedTreeId: list,
          );
        },
      ),
    );
    if (result is List<TreeEntity>) {
      if (result.length > 0) {
        controller.tree = result;
        onChanged?.call(result);
      } else {
        controller.tree = null;
        onChanged?.call(null);
      }
    }
  }
}

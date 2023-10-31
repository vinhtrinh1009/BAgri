import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';

import 'app_farmer_picker_page.dart';

class FarmerPickerController extends ValueNotifier<List<FarmerEntity>?> {
  FarmerPickerController({List<FarmerEntity>? farmerList}) : super(farmerList);

  List<FarmerEntity>? get farmerList => value;

  set farmerList(List<FarmerEntity>? farmerList) {
    value = farmerList;
    notifyListeners();
  }
}

class AppPageFarmerPicker extends StatelessWidget {
  final FarmerPickerController controller;
  final ValueChanged<List<FarmerEntity>?>? onChanged;

  final bool enabled;

  AppPageFarmerPicker({
    required this.controller,
    this.onChanged,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: controller,
      builder: (context, List<FarmerEntity>? farmerList, child) {
        String text = farmerList?[0].fullName ?? "";

        if (farmerList != null) {
          for (int i = 1; i < farmerList.length; i++)
            text += ', ${farmerList[i].fullName!}';
        }

        return GestureDetector(
          onTap: enabled
              ? () {
                  _showMyProjectPicker(context: context);
                }
              : null,
          child: Column(
            children: [
              Stack(
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
                      hintText: 'Chọn người thực hiện',
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
              SizedBox(
                height: 10,
              ),
              Container(
                child: Wrap(
                  spacing: 20,
                  alignment: WrapAlignment.start,
                  crossAxisAlignment: WrapCrossAlignment.start,
                  children: List.generate(farmerList?.length ?? 0, (index) {
                    return Container(
                      margin: EdgeInsets.all(5),
                      padding:
                          EdgeInsets.symmetric(vertical: 5, horizontal: 10),
                      decoration: BoxDecoration(
                          color: Color(0xFFC4C4C4),
                          borderRadius: BorderRadius.circular(25)),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Image.asset(
                            AppImages.icEmployeeAvatar,
                            width: 20,
                            height: 20,
                          ),
                          SizedBox(
                            width: 10,
                          ),
                          Text(farmerList![index].fullName!),
                        ],
                      ),
                    );
                  }),
                ),
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
          if (controller.farmerList != null) {
            for (FarmerEntity e in controller.farmerList!) {
              list.add(e.farmerId!);
            }
          }
          return AppFarmerPickerPage(
            selectedFarmerId: list,
          );
        },
      ),
    );
    if (result is List<FarmerEntity>) {
      if (result.length > 0) {
        controller.farmerList = result;
        onChanged?.call(result);
      } else {
        controller.farmerList = null;
        onChanged?.call(null);
      }
    }
  }
}

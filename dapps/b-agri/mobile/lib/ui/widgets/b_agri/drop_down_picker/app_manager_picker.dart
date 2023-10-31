import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/entities/manager/manager_entity.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AppManagerPicker extends StatefulWidget {
  String? hintText;
  AutovalidateMode? autoValidateMode;
  String? managerId;
  bool centerItem;
  TextStyle? textStyle;
  ValueChanged<ManagerEntity?>? onChange;
  // FormFieldValidator<String>? validator;
  AppManagerPicker(
      {Key? key,
      this.autoValidateMode,
      this.textStyle,
      this.hintText,
      this.managerId,
      this.onChange,
      // this.validator,
      this.centerItem = false})
      : super(key: key);

  @override
  State<AppManagerPicker> createState() => _AppManagerPickerState();
}

class _AppManagerPickerState extends State<AppManagerPicker> {
  late List<ManagerEntity> _managerList;
  late AppCubit _appCubit;
  ManagerEntity? value;

  @override
  void initState() {
    _appCubit = BlocProvider.of<AppCubit>(context);
    _managerList = _appCubit.state.managers!;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.managerId != null) {
      value = _managerList
          .firstWhere((element) => element.manager_id == widget.managerId);
    }
    return DropdownButtonFormField(
        value: value,
        autovalidateMode: widget.autoValidateMode,
        style: widget.textStyle ?? AppTextStyle.blackS16,
        icon: Padding(
            padding: const EdgeInsets.only(right: 10),
            child: Icon(Icons.keyboard_arrow_down)),
        onChanged: widget.onChange,
        decoration: InputDecoration(
          hintText: widget.hintText ?? 'Chọn quản lý',
          hintStyle: AppTextStyle.greyS14,
          contentPadding:
              EdgeInsets.only(top: 10, right: 10, bottom: 10, left: 20),
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
        ),
        isExpanded: true,
        items: _managerList.map((value) {
          return DropdownMenuItem<ManagerEntity>(
            alignment: widget.centerItem
                ? Alignment.center
                : AlignmentDirectional.centerStart,
            child: Text(value.fullname ?? ""),
            value: value,
          );
        }).toList());
  }
}

class AppCustomManagerPicker extends StatefulWidget {
  String? hintText;
  AutovalidateMode? autoValidateMode;
  String? managerId;
  bool centerItem;
  TextStyle? textStyle;
  ValueChanged<ManagerEntity?>? onChange;
  // FormFieldValidator<String>? validator;
  AppCustomManagerPicker(
      {Key? key,
      this.autoValidateMode,
      this.textStyle,
      this.hintText,
      this.managerId,
      this.onChange,
      // this.validator,
      this.centerItem = false})
      : super(key: key);

  @override
  State<AppCustomManagerPicker> createState() => _AppCustomManagerPickerState();
}

class _AppCustomManagerPickerState extends State<AppCustomManagerPicker> {
  late List<ManagerEntity> _managerList;
  late AppCubit _appCubit;
  ManagerEntity? value;

  @override
  void initState() {
    _managerList = [];
    _appCubit = BlocProvider.of<AppCubit>(context);
    _managerList.addAll(_appCubit.state.managers!);

    ManagerEntity allManagerObject =
        ManagerEntity(manager_id: "allManager", fullname: 'Tất cả');
    _managerList.insertAll(0, [allManagerObject]);

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.managerId != null) {
      value = _managerList
          .firstWhere((element) => element.manager_id == widget.managerId);
    }
    return DropdownButtonFormField(
        value: value,
        autovalidateMode: widget.autoValidateMode,
        style: widget.textStyle ?? AppTextStyle.blackS16,
        icon: Padding(
            padding: const EdgeInsets.only(right: 10),
            child: Icon(Icons.keyboard_arrow_down)),
        onChanged: widget.onChange,
        decoration: InputDecoration(
          hintText: widget.hintText ?? 'Chọn quản lý',
          hintStyle: AppTextStyle.greyS14,
          contentPadding:
              EdgeInsets.only(top: 10, right: 10, bottom: 10, left: 20),
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
        ),
        isExpanded: true,
        items: _managerList.map((value) {
          return DropdownMenuItem<ManagerEntity>(
            alignment: widget.centerItem
                ? Alignment.center
                : AlignmentDirectional.centerStart,
            child: Text(value.fullname ?? ""),
            value: value,
          );
        }).toList());
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:flutter_base/models/entities/role/role_entity.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AppDropDownButton extends StatelessWidget {
  String? hintText;
  List<String> itemList;
  ValueChanged<String?>? onChange;
  FormFieldValidator<String>? validator;
  AutovalidateMode? autoValidateMode;
  String? value;

  TextStyle? textStyle;
  AppDropDownButton({
    Key? key,
    this.hintText,
    required this.itemList,
    this.onChange,
    this.autoValidateMode,
    this.validator,
    this.textStyle,
    this.value,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField(
        value: value,
        autovalidateMode: autoValidateMode,
        style: textStyle ?? AppTextStyle.blackS14SemiBold,
        icon: Icon(Icons.keyboard_arrow_down),
        onChanged: onChange ?? (value) {},
        validator: validator,
        decoration: InputDecoration(
          isDense: true,
          hintText: hintText ?? "",
          hintStyle: AppTextStyle.greyS16,
          contentPadding: EdgeInsets.only(
            left: 20,
            right: 20,
            top: 13,
            bottom: 13,
          ),
          enabledBorder: OutlineInputBorder(
              borderSide: BorderSide(color: AppColors.main),
              borderRadius: BorderRadius.circular(10)),
          focusColor: AppColors.main,
          focusedBorder: OutlineInputBorder(
              borderSide: BorderSide(color: AppColors.main),
              borderRadius: BorderRadius.circular(10)),
          border: OutlineInputBorder(
              borderSide: BorderSide(color: AppColors.main),
              borderRadius: BorderRadius.circular(10)),
        ),
        isExpanded: true,
        items: itemList.map<DropdownMenuItem<String>>((String value) {
          return DropdownMenuItem(
            child: Text(
              value,
              style: AppTextStyle.blackS16,
            ),
            value: value,
          );
        }).toList());
  }
}

class AppTreePicker extends StatefulWidget {
  String? hintText;
  AutovalidateMode? autoValidateMode;
  TreeEntity? value;
  bool centerItem;
  TextStyle? textStyle;
  ValueChanged<TreeEntity?>? onChange;
  // FormFieldValidator<String>? validator;
  AppTreePicker(
      {Key? key,
      this.autoValidateMode,
      this.textStyle,
      this.hintText,
      this.value,
      this.onChange,
      // this.validator,
      this.centerItem = false})
      : super(key: key);

  @override
  State<AppTreePicker> createState() => _AppTreePickerState();
}

class _AppTreePickerState extends State<AppTreePicker> {
  late List<TreeEntity> _treeList;
  late AppCubit _appCubit;

  @override
  void initState() {
    _appCubit = BlocProvider.of<AppCubit>(context);
    _treeList = _appCubit.state.trees!;

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          height: 48,
          decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [AppShadow.appBoxShadow],
              borderRadius: BorderRadius.circular(5)),
        ),
        DropdownButtonFormField(
            value: widget.value,
            autovalidateMode: widget.autoValidateMode,
            style: widget.textStyle ?? AppTextStyle.blackS14SemiBold,
            icon: Padding(
                padding: const EdgeInsets.only(right: 10),
                child: Icon(Icons.keyboard_arrow_down)),
            onChanged: widget.onChange,
            decoration: InputDecoration(
              hintText: widget.hintText ?? 'Chọn loại cây',
              hintStyle: AppTextStyle.greyS14,
              contentPadding:
                  EdgeInsets.only(top: 10, right: 10, bottom: 10, left: 20),
              enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.mainDarker),
                  borderRadius: BorderRadius.circular(5)),
              focusColor: AppColors.main,
              focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.main),
                  borderRadius: BorderRadius.circular(5)),
              border: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.main),
                  borderRadius: BorderRadius.circular(5)),
            ),
            isExpanded: true,
            items: _treeList.map((value) {
              return DropdownMenuItem<TreeEntity>(
                alignment: widget.centerItem
                    ? Alignment.center
                    : AlignmentDirectional.centerStart,
                child: Text(value.name ?? ""),
                value: value,
              );
            }).toList()),
      ],
    );
  }
}

class AppGardenPicker extends StatefulWidget {
  String? hintText;
  AutovalidateMode? autoValidateMode;
  String? gardenId;
  bool centerItem;
  TextStyle? textStyle;
  ValueChanged<GardenEntity?>? onChange;
  // FormFieldValidator<String>? validator;
  AppGardenPicker(
      {Key? key,
      this.autoValidateMode,
      this.textStyle,
      this.hintText,
      this.gardenId,
      this.onChange,
      // this.validator,
      this.centerItem = false})
      : super(key: key);

  @override
  State<AppGardenPicker> createState() => _AppGardenPickerState();
}

class _AppGardenPickerState extends State<AppGardenPicker> {
  late List<GardenEntity> _gardenList;
  late AppCubit _appCubit;
  GardenEntity? value;

  @override
  void initState() {
    _appCubit = BlocProvider.of<AppCubit>(context);
    _gardenList = _appCubit.state.gardens!;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.gardenId != null) {
      value = _gardenList
          .firstWhere((element) => element.garden_id == widget.gardenId);
    }
    return Stack(
      children: [
        Container(
          height: 48,
          decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [AppShadow.appBoxShadow],
              borderRadius: BorderRadius.circular(5)),
        ),
        DropdownButtonFormField(
            value: value,
            autovalidateMode: widget.autoValidateMode,
            style: widget.textStyle ?? AppTextStyle.blackS14SemiBold,
            icon: Padding(
                padding: const EdgeInsets.only(right: 10),
                child: Icon(Icons.keyboard_arrow_down)),
            onChanged: widget.onChange,
            decoration: InputDecoration(
              hintText: widget.hintText ?? 'Chọn vườn',
              hintStyle: AppTextStyle.greyS14,
              contentPadding:
                  EdgeInsets.only(top: 10, right: 10, bottom: 10, left: 20),
              enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.mainDarker),
                  borderRadius: BorderRadius.circular(5)),
              focusColor: AppColors.main,
              focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.main),
                  borderRadius: BorderRadius.circular(5)),
              border: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.main),
                  borderRadius: BorderRadius.circular(5)),
            ),
            isExpanded: true,
            items: _gardenList.map((value) {
              return DropdownMenuItem<GardenEntity>(
                alignment: widget.centerItem
                    ? Alignment.center
                    : AlignmentDirectional.centerStart,
                child: Text(value.name ?? ""),
                value: value,
              );
            }).toList()),
      ],
    );
  }
}

class AppProcessPicker extends StatefulWidget {
  String? hintText;
  AutovalidateMode? autoValidateMode;
  ProcessEntity? value;
  bool centerItem;
  TextStyle? textStyle;
  ValueChanged<ProcessEntity?>? onChange;
  // FormFieldValidator<String>? validator;
  AppProcessPicker(
      {Key? key,
      this.autoValidateMode,
      this.textStyle,
      this.hintText,
      this.value,
      this.onChange,
      // this.validator,
      this.centerItem = false})
      : super(key: key);

  @override
  State<AppProcessPicker> createState() => _AppProcessPickerState();
}

class _AppProcessPickerState extends State<AppProcessPicker> {
  late List<ProcessEntity> _processList;
  late AppCubit _appCubit;

  @override
  void initState() {
    _appCubit = BlocProvider.of<AppCubit>(context);
    _processList = _appCubit.state.processes!;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          height: 48,
          decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [AppShadow.appBoxShadow],
              borderRadius: BorderRadius.circular(5)),
        ),
        DropdownButtonFormField(
            value: widget.value,
            autovalidateMode: widget.autoValidateMode,
            style: widget.textStyle ?? AppTextStyle.blackS14SemiBold,
            icon: Padding(
                padding: const EdgeInsets.only(right: 10),
                child: Icon(Icons.keyboard_arrow_down)),
            onChanged: widget.onChange,
            decoration: InputDecoration(
              hintText: widget.hintText ?? 'Chọn quy trình chăm sóc',
              hintStyle: AppTextStyle.greyS14,
              contentPadding:
                  EdgeInsets.only(top: 10, right: 10, bottom: 10, left: 20),
              enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.mainDarker),
                  borderRadius: BorderRadius.circular(5)),
              focusColor: AppColors.main,
              focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.main),
                  borderRadius: BorderRadius.circular(5)),
              border: OutlineInputBorder(
                  borderSide: BorderSide(color: AppColors.main),
                  borderRadius: BorderRadius.circular(5)),
            ),
            isExpanded: true,
            items: _processList.map((value) {
              return DropdownMenuItem<ProcessEntity>(
                alignment: widget.centerItem
                    ? Alignment.center
                    : AlignmentDirectional.centerStart,
                child: Text(value.name ?? ""),
                value: value,
              );
            }).toList()),
      ],
    );
  }
}

class AppRolePicker extends StatefulWidget {
  String? hintText;
  AutovalidateMode? autoValidateMode;
  RoleEntity? value;
  bool centerItem;
  TextStyle? textStyle;
  ValueChanged<RoleEntity?>? onChange;
  FormFieldValidator<RoleEntity>? validator;
  AppRolePicker(
      {Key? key,
      this.autoValidateMode,
      this.textStyle,
      this.hintText,
      this.value,
      this.onChange,
      this.validator,
      this.centerItem = false})
      : super(key: key);

  @override
  State<AppRolePicker> createState() => _AppRolePickerState();
}

class _AppRolePickerState extends State<AppRolePicker> {
  late List<RoleEntity> _roleList;

  @override
  void initState() {
    _roleList = [
      RoleEntity(role_id: "ktv", name: "Kỹ Thuật Viên"),
      RoleEntity(role_id: "qlv", name: "Quản Lý Vườn")
    ];

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          height: 48,
          decoration: BoxDecoration(
              color: Colors.white, borderRadius: BorderRadius.circular(10)),
        ),
        DropdownButtonFormField(
            validator: widget.validator,
            value: widget.value,
            autovalidateMode: widget.autoValidateMode,
            style: widget.textStyle ?? AppTextStyle.blackS14SemiBold,
            icon: Padding(
                padding: const EdgeInsets.only(right: 10),
                child: Icon(Icons.keyboard_arrow_down)),
            onChanged: widget.onChange,
            decoration: InputDecoration(
              hintText: widget.hintText ?? 'Chọn vai trò',
              hintStyle: AppTextStyle.greyS14,
              contentPadding:
                  EdgeInsets.only(top: 10, right: 10, bottom: 10, left: 20),
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
            ),
            isExpanded: true,
            items: _roleList.map((value) {
              return DropdownMenuItem<RoleEntity>(
                alignment: widget.centerItem
                    ? Alignment.center
                    : AlignmentDirectional.centerStart,
                child: Text(value.name ?? ""),
                value: value,
              );
            }).toList()),
      ],
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_shadow.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

class AppTextField extends StatelessWidget {
  final String labelText;
  final String hintText;
  final TextEditingController? controller;
  final ValueChanged<String>? onChanged;
  final FormFieldValidator<String>? validator;
  final TextInputType keyboardType;
  final FormFieldSetter<String>? onSaved;
  final bool? isRequire;
  final bool? enable;
  final TextStyle? labelStyle;
  final AutovalidateMode? autoValidateMode;
  final String? initialValue;
  final bool? obscureText;

  const AppTextField({
    Key? key,
    this.initialValue,
    this.labelText = '',
    this.hintText = '',
    this.controller,
    this.onChanged,
    this.keyboardType = TextInputType.text,
    this.autoValidateMode,
    this.validator,
    this.onSaved,
    this.isRequire,
    this.labelStyle,
    this.enable,
    this.obscureText = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      obscureText: obscureText!,
      obscuringCharacter: "*",
      enabled: enable,
      controller: controller,
      decoration: InputDecoration(
        hintText: hintText,
        contentPadding: const EdgeInsets.only(
          left: 20,
          right: 20,
          top: 13,
          bottom: 13,
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
        hintStyle: AppTextStyle.greyS16,
        isDense: true,
      ),
      initialValue: initialValue,
      autovalidateMode: autoValidateMode,
      validator: validator,
      keyboardType: keyboardType,
      onChanged: onChanged,
      style: AppTextStyle.blackS16,
      onSaved: onSaved,
    );
  }
}

class AppTextFieldUnderLine extends StatelessWidget {
  final String labelText;
  final String hintText;
  final TextEditingController? controller;
  final ValueChanged<String>? onChanged;
  final FormFieldValidator<String>? validator;
  final TextInputType keyboardType;
  final FormFieldSetter<String>? onSaved;
  final bool? isRequire;
  final TextStyle? labelStyle;
  final AutovalidateMode? autoValidateMode;
  final String? initialValue;
  final bool? enable;

  const AppTextFieldUnderLine({
    Key? key,
    this.initialValue,
    this.labelText = '',
    this.hintText = '',
    this.controller,
    this.onChanged,
    this.keyboardType = TextInputType.number,
    this.autoValidateMode,
    this.validator,
    this.onSaved,
    this.isRequire,
    this.labelStyle,
    this.enable,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          height: 25,
          padding: EdgeInsets.symmetric(horizontal: 20),
          child: TextFormField(
            enabled: enable,
            controller: controller,
            decoration: InputDecoration(
              hintText: hintText,
              contentPadding:
                  const EdgeInsets.only(left: 2, right: 2, bottom: 12),
              enabledBorder: UnderlineInputBorder(
                borderSide: BorderSide(color: Color(0xFF000000)),
              ),
              focusedBorder: UnderlineInputBorder(
                borderSide: BorderSide(color: Color(0xFF000000)),
              ),
              // hintStyle: AppTextStyle.greyS16,
            ),
            initialValue: initialValue,
            autovalidateMode: autoValidateMode,
            validator: validator,
            keyboardType: keyboardType,
            onChanged: onChanged,
            style: AppTextStyle.blackS14,
            onSaved: onSaved,
          ),
        ),
      ],
    );
  }
}

class AppTextAreaField extends StatelessWidget {
  final String labelText;
  final String hintText;
  final TextEditingController? controller;
  final ValueChanged<String>? onChanged;
  final FormFieldValidator<String>? validator;
  final TextInputType keyboardType;
  final FormFieldSetter<String>? onSaved;
  final bool? isRequire;
  final TextStyle? labelStyle;
  final AutovalidateMode? autoValidateMode;
  final String? initialValue;
  final int? maxLines;
  final bool? enable;

  const AppTextAreaField({
    Key? key,
    this.maxLines,
    this.initialValue,
    this.labelText = '',
    this.hintText = '',
    this.controller,
    this.onChanged,
    this.keyboardType = TextInputType.text,
    this.autoValidateMode,
    this.validator,
    this.onSaved,
    this.isRequire,
    this.labelStyle,
    this.enable,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Stack(
          children: [
            Container(
              decoration: BoxDecoration(
                  color: enable == true ? Colors.white : Colors.grey,
                  // boxShadow: [AppShadow.appBoxShadow],
                  borderRadius: BorderRadius.circular(5)),
            ),
            TextFormField(
              enabled: enable,
              maxLines: maxLines,
              controller: controller,
              decoration: InputDecoration(
                hintText: hintText,
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
                // hintStyle: AppTextStyle.greyS16,
              ),
              initialValue: initialValue,
              autovalidateMode: autoValidateMode,
              validator: validator,
              keyboardType: keyboardType,
              onChanged: onChanged,
              style: AppTextStyle.blackS14,
              onSaved: onSaved,
            ),
          ],
        ),
      ],
    );
  }
}

class AppLoginField extends StatelessWidget {
  final String labelText;
  final String hintText;
  final TextEditingController? controller;
  final ValueChanged<String>? onChanged;
  final FormFieldValidator<String>? validator;
  final TextInputType keyboardType;
  final FormFieldSetter<String>? onSaved;
  final bool? isRequire;
  final bool? enable;
  final TextStyle? labelStyle;
  final AutovalidateMode? autoValidateMode;
  final String? initialValue;
  final bool? obscureText;

  const AppLoginField({
    Key? key,
    this.initialValue,
    this.labelText = '',
    this.hintText = '',
    this.controller,
    this.onChanged,
    this.keyboardType = TextInputType.text,
    this.autoValidateMode,
    this.validator,
    this.onSaved,
    this.isRequire,
    this.labelStyle,
    this.enable,
    this.obscureText = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          height: 48,
          decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                const BoxShadow(
                  color: AppColors.inputFieldEnabledBorder,
                  blurRadius: 1,
                  offset: Offset(1, 1),
                ),
              ],
              borderRadius: BorderRadius.circular(25)),
        ),
        TextFormField(
          obscureText: obscureText!,
          obscuringCharacter: "*",
          enabled: enable,
          controller: controller,
          decoration: InputDecoration(
            hintText: hintText,
            contentPadding: const EdgeInsets.only(
              left: 20,
              right: 15,
              top: 10,
              bottom: 10,
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(25),
              borderSide: BorderSide(color: AppColors.redTextButton),
            ),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(25),
              borderSide: BorderSide(color: AppColors.lineGray),
            ),
            disabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: AppColors.mainDarker),
                borderRadius: BorderRadius.circular(25)),
            enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: AppColors.mainDarker),
                borderRadius: BorderRadius.circular(25)),
            focusedBorder: OutlineInputBorder(
                borderSide: BorderSide(color: AppColors.mainDarker),
                borderRadius: BorderRadius.circular(25)),
            hintStyle: AppTextStyle.greyS14,
          ),
          initialValue: initialValue,
          autovalidateMode: autoValidateMode,
          validator: validator,
          keyboardType: keyboardType,
          onChanged: onChanged,
          style: AppTextStyle.blackS14,
          onSaved: onSaved,
        ),
      ],
    );
  }
}

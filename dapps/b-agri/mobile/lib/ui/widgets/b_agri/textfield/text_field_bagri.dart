import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

class BagriLabelTextField extends StatefulWidget {
  final String? labelText;
  final TextStyle? labelStyle;
  final String highlightText;
  final Widget? suffixIcon;
  final BoxConstraints? suffixIconConstraints;
  final TextEditingController? textEditingController;
  final TextStyle? textStyle;
  final String? hintText;
  final TextStyle? hintStyle;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final TextInputType textInputType;
  final FormFieldValidator<String>? validator;
  final List<TextInputFormatter>? inputFormatters;
  final bool enabled;
  final int? maxLength;
  final double? labelInputDistance;

  BagriLabelTextField({
    this.labelText,
    this.labelStyle,
    this.highlightText = "*",
    this.suffixIcon,
    this.suffixIconConstraints,
    this.textEditingController,
    this.textStyle,
    this.hintText,
    this.hintStyle,
    this.onChanged,
    this.labelInputDistance,
    this.onSubmitted,
    this.textInputType = TextInputType.text,
    this.validator,
    this.inputFormatters,
    this.enabled = true,
    this.maxLength,
  });

  @override
  State<BagriLabelTextField> createState() => _BagriLabelTextFieldState();
}

class _BagriLabelTextFieldState extends State<BagriLabelTextField> {
  bool _startCheckValid = false;
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            child: (widget.highlightText != "" &&
                    widget.highlightText.isNotEmpty)
                ? RichText(
                    text: TextSpan(children: [
                      TextSpan(
                        text: widget.labelText ?? "",
                        style: widget.labelStyle ?? AppTextStyle.blackS12,
                      ),
                      TextSpan(
                        text: widget.highlightText,
                        style:
                            AppTextStyle.blackS12.copyWith(color: Colors.red),
                      )
                    ]),
                  )
                : Text(widget.labelText ?? "",
                    style: widget.labelStyle ?? AppTextStyle.blackS12),
          ),
          SizedBox(
            height: widget.labelInputDistance ?? 0,
          ),
          Container(
            margin: EdgeInsets.symmetric(vertical: 5),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                const BoxShadow(
                  color: Colors.grey,
                  blurRadius: 4,
                  spreadRadius: 0.01,
                  offset: Offset(0, 5),
                ),
              ],
              borderRadius: BorderRadius.circular(5.0),
            ),
            child: TextField(
              onTap: () {
                setState(() {
                  _startCheckValid = true;
                });
              },
              enabled: widget.enabled,
              onSubmitted: widget.onSubmitted,
              onChanged: widget.onChanged,
              controller: widget.textEditingController,
              style: widget.enabled
                  ? widget.textStyle ?? AppTextStyle.blackS16
                  : (widget.textStyle ?? AppTextStyle.greyS16)
                      .copyWith(color: AppColors.gray),
              maxLines: 1,
              maxLength: widget.maxLength,
              decoration: InputDecoration(
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.all(Radius.circular(5.0)),
                  borderSide: BorderSide(width: 1.75 ,color: AppColors.inputFieldEnabledBorder),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.all(Radius.circular(5.0)),
                  borderSide: BorderSide(width: 1.75 ,color: AppColors.inputFieldEnabledBorder),
                ),
                disabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.all(Radius.circular(5.0)),
                  borderSide: BorderSide(width: 1.75 ,color: AppColors.inputFieldEnabledBorder),
                ),
                fillColor: Colors.white,
                hintStyle: widget.hintStyle ?? AppTextStyle.greyS16,
                hintText: widget.hintText ?? "",
                isDense: true,
                contentPadding: EdgeInsets.only(top: 8, bottom: 12, left: 12, right: 12),
                suffixIcon: widget.suffixIcon,
                suffixIconConstraints: widget.suffixIconConstraints ??
                    BoxConstraints(maxHeight: 32, maxWidth: 32),
                counterText: "",

              ),
              cursorColor: AppColors.gray,
              keyboardType: widget.textInputType,
              inputFormatters: widget.inputFormatters,
            ),
          ),
          widget.textEditingController != null
              ? ValueListenableBuilder(
                  valueListenable: widget.textEditingController!,
                  builder: (context, TextEditingValue controller, child) {
                    final isValid =
                        widget.validator?.call(controller.text) ?? "";
                    return Column(
                      children: [
                        SizedBox(height: 2),
                        Text(
                          _startCheckValid ? isValid : "",
                          style:
                              AppTextStyle.blackS12.copyWith(color: Colors.red),
                        ),
                        SizedBox(height: 12),
                      ],
                    );
                  },
                )
              : Container(),
        ],
      ),
    );
  }
}

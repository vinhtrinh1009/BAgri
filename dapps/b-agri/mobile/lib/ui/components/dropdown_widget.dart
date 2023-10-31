import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';

class DropDownWidget extends StatefulWidget {
  final String? title;
  final List<String>? listDropDown;
  final String? value;
  final Function? selectCallBack;
  final TextStyle? textStyle;
  final isBorder;
  final String? highlightText;
  final bool isRequired;

  DropDownWidget({
    this.listDropDown,
    this.title,
    this.value,
    this.selectCallBack,
    this.textStyle,
    this.isBorder = true,
    this.highlightText = "*",
    this.isRequired = false,
  });

  @override
  _DropDownWidgetState createState() => _DropDownWidgetState();
}

class _DropDownWidgetState extends State<DropDownWidget> {
  String? _value;

  @override
  void initState() {
    super.initState();
    if (widget.value != null) _value = widget.value;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        widget.isRequired
            ? Container(
                child: RichText(
                  text: TextSpan(children: [
                    TextSpan(
                      text: widget.title ?? "",
                      style: widget.textStyle ??
                          TextStyle(
                            color: AppColors.buttonTint,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    TextSpan(
                      text: widget.highlightText ?? "",
                      style: AppTextStyle.blackS12.copyWith(color: Colors.red),
                    )
                  ]),
                ),
              )
            : Text(
                widget.title!,
                style: widget.textStyle ??
                    TextStyle(
                      color: AppColors.buttonTint,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
              ),
        Container(
          margin: EdgeInsets.only(top: widget.isRequired ? 0 : 8),
          decoration: widget.isBorder
              ? BoxDecoration(
                  border: Border.all(color: Colors.grey, width: 1),
                  borderRadius: BorderRadius.circular(6),
                )
              : BoxDecoration(
                  border: Border(
                    bottom:
                        BorderSide(color: AppColors.textFieldDisabledBorder),
                  ),
                ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: _value,
              isExpanded: true,
              icon: Icon(
                Icons.keyboard_arrow_down,
                color: Colors.grey,
              ),
              onChanged: (String? newValue) {
                setState(() {
                  _value = newValue;
                  widget.selectCallBack!(newValue);
                });
              },
              items: widget.listDropDown!
                  .map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Container(
                    child: Text(
                      value,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                );
              }).toList(),
              hint: Text(
                "Chọn YCDCH",
              ),
            ),
          ),
        ),
      ],
    );
  }
}

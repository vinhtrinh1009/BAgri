import 'package:flutter/material.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/ui/widgets/b_agri/textfield/text_field_bagri.dart';
import 'package:flutter_base/utils/validators.dart';

class BagriInput extends BagriLabelTextField {
  BagriInput({
    String? highlightText,
    TextEditingController? textEditingController,
    ValueChanged<String>? onChanged,
    bool enabled = true,
    TextStyle? textStyle,
    TextStyle? labelStyle,
    bool? checkValid = true,
    String? labelText,
    String? hintText,
    String? errorText,
  }) : super(
          textEditingController: textEditingController,
          onChanged: onChanged,
          labelText: labelText,
          labelStyle: labelStyle,
          hintText: "",
          highlightText: highlightText ?? "",
          textStyle: textStyle,
          textInputType: TextInputType.text,
          enabled: enabled,
          validator: (text) {
            if (Validator.validateFullName(text!) || checkValid == false) {
              return "";
            } else if (text.length == 0)
              return hintText;
            else {
              return errorText;
            }
          },
        );
}

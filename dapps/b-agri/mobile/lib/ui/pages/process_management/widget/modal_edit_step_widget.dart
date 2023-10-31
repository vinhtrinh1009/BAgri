import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_base/utils/validators.dart';

class ModalEditStepWidget extends StatefulWidget {
  const ModalEditStepWidget({
    Key? key,
    required this.phase,
    this.name,
    this.stepId,
    this.actualDay,
    this.endDate,
    this.startDate,
    required this.onPressed,
    this.onDelete,
  }) : super(key: key);

  final void Function(String name, String startDate, String endDate,
      String stepId, String duration) onPressed;
  final String? phase;
  final String? name;
  final String? stepId;
  final String? actualDay;
  final String? startDate;
  final String? endDate;
  final VoidCallback? onDelete;

  @override
  State<ModalEditStepWidget> createState() => _ModalEditStepWidgetState();
}

class _ModalEditStepWidgetState extends State<ModalEditStepWidget> {
  final _formKey = GlobalKey<FormState>();

  TextEditingController nameController = TextEditingController(text: '');
  TextEditingController startDateController = TextEditingController(text: '');
  TextEditingController endDateController = TextEditingController(text: '');
  TextEditingController stepController = TextEditingController(text: '');
  TextEditingController actualDayController = TextEditingController(text: '');
  late double heightResize = 0.5;

  @override
  void initState() {
    super.initState();

    nameController = TextEditingController(text: widget.name);
    startDateController = TextEditingController(text: widget.startDate);
    endDateController = TextEditingController(text: widget.endDate);
    stepController = TextEditingController(text: widget.stepId);
    actualDayController = TextEditingController(text: widget.actualDay);
  }

  @override
  Widget build(BuildContext context) {
    FocusScopeNode currentScope = FocusScope.of(context);
    final viewInsetsBottom = MediaQuery.of(context).viewInsets.bottom;
    if (viewInsetsBottom == 0 || currentScope.hasPrimaryFocus == true) {
      setState(() {
        heightResize = 0.5;
      });
    } else {
      setState(() {
        heightResize = 0.9;
      });
    }

    return Container(
      height: MediaQuery.of(context).size.height * heightResize,
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: new BorderRadius.only(
              topLeft: const Radius.circular(20),
              topRight: const Radius.circular(20))),
      child: Column(
        children: [
          Container(
            decoration: BoxDecoration(
                color: Color(0xFFECE5D5),
                borderRadius: new BorderRadius.only(
                    topLeft: const Radius.circular(20),
                    topRight: const Radius.circular(20))),
            height: 40,
            child: Stack(
              children: [
                Container(
                    width: double.infinity,
                    height: 40,
                    padding: EdgeInsets.all(10),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          '${nameController.text}',
                          style: TextStyle(
                              color: Color(0xFF1F1E1C),
                              fontWeight: FontWeight.bold,
                              fontSize: 16),
                        ),
                      ],
                    )),
                Align(
                  alignment: Alignment.centerLeft,
                  child: Container(
                      height: 40,
                      padding: EdgeInsets.all(10),
                      child: Text('Giai đoạn ${widget.phase}')),
                ),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 8, vertical: 5),
                  child: Align(
                    alignment: Alignment.topRight,
                    child: GestureDetector(
                      onTap: () {
                        Navigator.of(context).pop();
                      },
                      child: Image.asset(
                        AppImages.icCloseCircleShadow,
                        height: 25,
                        width: 25,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(
            height: 20,
          ),
          Expanded(
            child: Container(
              margin: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
              child: Form(
                key: _formKey,
                child: Column(children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'Từ ${startDateController.text} ngày',
                        style:
                            TextStyle(color: Color(0xFF1F1E1C), fontSize: 16),
                      ),
                      SizedBox(
                        width: 30,
                      ),
                      Text(
                        'Đến ${endDateController.text} ngày',
                        style:
                            TextStyle(color: Color(0xFF1F1E1C), fontSize: 16),
                      ),
                    ],
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  Row(
                    children: [
                      Expanded(
                        child: AppTextField(
                          autoValidateMode: AutovalidateMode.onUserInteraction,
                          hintText: 'Thời gian thực hiện',
                          keyboardType: TextInputType.number,
                          controller: actualDayController,
                          validator: (value) {
                            if (Validator.validateNullOrEmpty(value!))
                              return "Chưa nhập thời gian thực hiện";
                            else if (int.parse(value) <
                                    int.parse(startDateController.text) ||
                                int.parse(value) >
                                    int.parse(endDateController.text)) {
                              return "Thời gian thực hiện phải từ ${startDateController.text} đến ${endDateController.text} ngày";
                            } else {
                              return null;
                            }
                          },
                        ),
                      ),
                    ],
                  ),
                  SizedBox(
                    height: 40,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Expanded(
                        child: AppButton(
                          color: AppColors.redButton,
                          title: 'Xóa bước',
                          onPressed: () {
                            Navigator.of(context).pop();
                            widget.onDelete!();
                          },
                        ),
                      ),
                      SizedBox(width: 20),
                      Expanded(
                        child: AppButton(
                            color: AppColors.main,
                            title: 'Xác nhận',
                            onPressed: () {
                              if (_formKey.currentState!.validate()) {
                                Navigator.of(context).pop();
                                widget.onPressed(
                                  nameController.text,
                                  startDateController.text,
                                  endDateController.text,
                                  stepController.text,
                                  actualDayController.text,
                                );
                              }
                            }),
                      ),
                    ],
                  ),
                ]),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

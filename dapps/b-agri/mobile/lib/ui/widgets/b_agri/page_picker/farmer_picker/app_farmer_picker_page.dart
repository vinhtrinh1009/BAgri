import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';

import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../app_button.dart';
import '../../app_circular_progress_indicator.dart';

class AppFarmerPickerPage extends StatefulWidget {
  final List<String> selectedFarmerId;

  AppFarmerPickerPage({required this.selectedFarmerId});

  @override
  _AppFarmerPickerPageState createState() => _AppFarmerPickerPageState();
}

class _AppFarmerPickerPageState extends State<AppFarmerPickerPage> {
  late AppCubit _cubit;
  List<FarmerEntity> selectedFarmer = [];

  @override
  void initState() {
    _cubit = BlocProvider.of<AppCubit>(context);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Chọn người thực hiện',
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(child: _buildListResult()),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                AppButton(
                  color: AppColors.redButton,
                  title: 'Hủy bỏ',
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
                SizedBox(width: 50),
                AppButton(
                  width: 100,
                  color: AppColors.main,
                  title: 'Xác nhận',
                  onPressed: () async {
                    Navigator.of(context).pop(selectedFarmer);
                  },
                ),
              ],
            ),
            SizedBox(height: 50),
          ],
        ),
      ),
    );
  }

  Widget _buildListResult() {
    return BlocBuilder<AppCubit, AppState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return prev.farmerStatus != current.farmerStatus;
      },
      builder: (context, state) {
        if (state.farmerStatus == LoadStatus.LOADING) {
          return Center(
            child: AppCircularProgressIndicator(),
          );
        } else {
          return ListView.separated(
            itemCount: (state.farmers)?.length ?? 0,
            shrinkWrap: true,
            primary: false,
            separatorBuilder: (context, index) {
              return Container(
                height: 1,
                color: Colors.grey.withOpacity(0.3),
                margin: EdgeInsets.symmetric(horizontal: 10),
              );
            },
            itemBuilder: (context, index) {
              final farmer = state.farmers![index];
              String title = farmer.fullName!;
              bool isSelected = false;

              for (String e in widget.selectedFarmerId) {
                if (e == farmer.farmerId) {
                  isSelected = true;
                  selectedFarmer.add(farmer);
                }
              }

              return ItemWidget(
                  title: title,
                  isSelected: isSelected,
                  onTap: (value) {
                    if (value) {
                      selectedFarmer.add(farmer);
                    } else {
                      selectedFarmer.remove(farmer);
                    }
                  });
            },
          );
        }
      },
    );
  }
}

class ItemWidget extends StatefulWidget {
  String title;
  bool isSelected;
  Function(bool value) onTap;
  ItemWidget({
    Key? key,
    required this.title,
    required this.isSelected,
    required this.onTap,
  }) : super(key: key);

  @override
  State<ItemWidget> createState() => _ItemWidgetState();
}

class _ItemWidgetState extends State<ItemWidget> {
  late bool check;
  @override
  void initState() {
    super.initState();
    check = widget.isSelected;
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        setState(() {
          check = !check;
          widget.onTap(check);
        });
      },
      child: Container(
        color: Colors.white,
        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Row(
          children: [
            Expanded(
              flex: 8,
              child: Text(
                widget.title,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Visibility(
              visible: check,
              maintainSize: true,
              maintainAnimation: true,
              maintainState: true,
              child: Icon(
                Icons.check,
                color: AppColors.main,
              ),
            )
          ],
        ),
      ),
    );
  }
}

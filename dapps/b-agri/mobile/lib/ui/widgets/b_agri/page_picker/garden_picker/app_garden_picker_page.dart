import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';

import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_html/shims/dart_ui.dart';

import '../../app_button.dart';
import '../../app_circular_progress_indicator.dart';

class AppGardenPickerPage extends StatefulWidget {
  final String? selectedGardenId;

  AppGardenPickerPage({this.selectedGardenId});

  @override
  _AppGardenPickerPageState createState() => _AppGardenPickerPageState();
}

class _AppGardenPickerPageState extends State<AppGardenPickerPage> {
  late AppCubit _cubit;
  GardenEntity? selectedGarden;

  @override
  void initState() {
    _cubit = BlocProvider.of<AppCubit>(context);
    super.initState();
    _cubit.fetchListGarden();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Chọn vườn',
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(child: _buildListResult()),
          ],
        ),
      ),
    );
  }

  Widget _buildListResult() {
    return BlocBuilder<AppCubit, AppState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return prev.getGardenStatus != current.getGardenStatus;
      },
      builder: (context, state) {
        if (state.getGardenStatus == LoadStatus.LOADING) {
          return Center(
            child: AppCircularProgressIndicator(),
          );
        } else {
          return ListView.separated(
            padding: EdgeInsets.only(top: 10),
            itemCount: (state.gardens)?.length ?? 0,
            shrinkWrap: true,
            primary: false,
            separatorBuilder: (context, index) {
              return SizedBox(height: 10);
            },
            itemBuilder: (context, index) {
              final garden = state.gardens![index];
              String title = garden.name!;
              bool isSelected = false;
              if (widget.selectedGardenId != null) if (garden.garden_id ==
                  widget.selectedGardenId) isSelected = true;
              return ItemWidget(
                  title: title,
                  isSelected: isSelected,
                  onTap: () {
                    Navigator.of(context).pop(garden);
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
  VoidCallback onTap;
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
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: widget.onTap,
      child: Container(
        padding: EdgeInsets.only(top: 10, bottom: 10, left: 25, right: 10),
        decoration: BoxDecoration(
            color: AppColors.grayEC, borderRadius: BorderRadius.circular(10)),
        margin: EdgeInsets.symmetric(horizontal: 12),
        child: Row(
          children: [
            Expanded(
              flex: 8,
              child: Text(
                widget.title,
                style: AppTextStyle.blackS18,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Visibility(
              visible: widget.isSelected,
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

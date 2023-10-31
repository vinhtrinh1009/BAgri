import 'package:flutter/material.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/ui/pages/garden_management/garden_task/season_step/season_step_cubit.dart';

import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/garden_picker/app_garden_picker_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../app_circular_progress_indicator.dart';

class AppStepPickerPage extends StatefulWidget {
  final String? selectedStepId;
  final String seasonId;
  AppStepPickerPage({this.selectedStepId, required this.seasonId});

  @override
  _AppStepPickerPageState createState() => _AppStepPickerPageState();
}

class _AppStepPickerPageState extends State<AppStepPickerPage> {
  late SeasonStepCubit _cubit;
  StepEntity? selectedStep;
  late List<StepEntity> _listStep;
  @override
  void initState() {
    _cubit = BlocProvider.of<SeasonStepCubit>(context);
    super.initState();
    print('seasonId ${widget.seasonId}');
    _cubit.getListSeasonSteps(widget.seasonId);

    _listStep = [
      StepEntity(step_id: "620cab64d337e9856fbcbc44", name: "Ươm hạt"),
      StepEntity(step_id: "620cab64d337e9856fbcbc45", name: "Trồng cây")
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Chọn bước',
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
    return BlocBuilder<SeasonStepCubit, SeasonStepState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return prev.loadStatus != current.loadStatus;
      },
      builder: (context, state) {
        if (state.loadStatus == LoadStatus.LOADING) {
          return Center(
            child: AppCircularProgressIndicator(),
          );
        } else {
          return ListView.separated(
            padding: EdgeInsets.only(top: 10),
            itemCount: (state.steps)?.length ?? 0,
            // itemCount: (_listStep).length,
            shrinkWrap: true,
            primary: false,
            separatorBuilder: (context, index) {
              return SizedBox(height: 10);
            },
            itemBuilder: (context, index) {
              final step = state.steps![index];
              // final step = _listStep[index];

              String title = step.name!;
              bool isSelected = false;
              if (widget.selectedStepId != null) if (step.step_id ==
                  widget.selectedStepId) isSelected = true;
              return ItemWidget(
                  title: title,
                  isSelected: isSelected,
                  onTap: () {
                    Navigator.of(context).pop(step);
                  });
            },
          );
        }
      },
    );
  }
}

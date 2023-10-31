part of 'season_step_cubit.dart';

class SeasonStepState extends Equatable {
  List<StepEntity>? steps;
  LoadStatus? loadStatus;

  @override
  List<Object?> get props => [
        this.steps,
        this.loadStatus,
      ];

  SeasonStepState({
    this.steps,
    this.loadStatus,
  });

  SeasonStepState copyWith({
    List<StepEntity>? steps,
    LoadStatus? loadStatus,
  }) {
    return SeasonStepState(
      steps: steps ?? this.steps,
      loadStatus: loadStatus ?? this.loadStatus,
    );
  }
}

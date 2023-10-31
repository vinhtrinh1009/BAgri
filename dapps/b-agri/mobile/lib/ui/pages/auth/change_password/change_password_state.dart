part of 'change_password_cubit.dart';

class ChangePasswordState extends Equatable {
  LoadStatus? loadStatus;

  @override
  List<Object?> get props => [
        this.loadStatus,
      ];

  ChangePasswordState({
    this.loadStatus,
  });

  ChangePasswordState copyWith({
    LoadStatus? loadStatus,
  }) {
    return ChangePasswordState(
      loadStatus: loadStatus ?? this.loadStatus,
    );
  }
}

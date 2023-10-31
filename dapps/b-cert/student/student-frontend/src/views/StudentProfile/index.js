import { Grid } from "@material-ui/core";
import View from "../../shared/View";
import ProfileForm from "./ProfileForm";
import AvatarBar from "./AvatarBar";

export default function StudentProfile() {
  return (
    <div>
      <View title="Thông tin cá nhân">
        <Grid container spacing={4}>
          <Grid item xs={12} md={8}>
            <ProfileForm></ProfileForm>
          </Grid>
          <Grid item xs={12} md={4}>
            <AvatarBar></AvatarBar>
          </Grid>
        </Grid>
      </View>
    </div>
  );
}

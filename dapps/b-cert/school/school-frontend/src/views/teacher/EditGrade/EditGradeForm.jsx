import { Button, Grid, TextField, Typography } from "@material-ui/core";
import { useState } from "react";

export default function EditGradeForm({ hdSubmit, index, recordId, oldMidtermScore, oldFinalScore }) {
  const [midScore, setMidCore] = useState(oldMidtermScore)
  const [finalScore, setFinalScore] = useState(oldFinalScore)
  console.log(oldMidtermScore, oldFinalScore)
  return (
    <Grid container justify="space-between" alignItems="center">
      <Grid item xs={12} md={3}>
        <Typography variant="h4">Nhập điểm mới:</Typography>
      </Grid>
      <Grid item xs={12} md={4}>
        <TextField
          id={"Mid" + index}
          variant="outlined"
          color="primary"
          size="small"
          label="Điểm GK"
          value={midScore}
          onChange={(e) => setMidCore(e.target.value)}
        ></TextField>
      </Grid>
      <Grid item xs={12} md={4}>
        <TextField
          variant="outlined"
          color="primary"
          size="small"
          label="Điểm CK"
          value={finalScore}
          onChange={(e) => setFinalScore(e.target.value)}
        ></TextField>
      </Grid>
      <Grid item xs={12} md={1}>
        <Button
          variant="contained"
          color="primary"
          onClick={(e) => {
            hdSubmit(recordId, midScore, finalScore);
          }
          }
        >
          Submit
        </Button>
      </Grid>
    </Grid>
  );
}

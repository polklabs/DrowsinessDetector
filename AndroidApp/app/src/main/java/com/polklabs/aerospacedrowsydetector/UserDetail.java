package com.polklabs.aerospacedrowsydetector;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.helper.StaticLabelsFormatter;
import com.jjoe64.graphview.series.BarGraphSeries;
import com.jjoe64.graphview.series.DataPoint;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class UserDetail extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    boolean doubleBackToExitPressedOnce = false;

    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference ref;
    FirebaseAuth mAuth = FirebaseAuth.getInstance();
    String currentUser;
    DataSnapshot userSnapshot;
    Toolbar toolbar;

    //Content widgets
    TextView blinkFreq;

    TextView EyeTitle;
    ToggleButton EyeDay;
    ToggleButton EyeHour;
    ToggleButton EyeTime;
    GraphView EyeGraph;
    LinearLayout EyeTimestamps;

    TextView YawnTitle;
    ToggleButton YawnDay;
    ToggleButton YawnHour;
    ToggleButton YawnTime;
    GraphView YawnGraph;
    LinearLayout YawnTimestamps;

    Map<String, Integer> eyeDay;
    Map<String, Integer> eyeWeek;
    Map<String, Integer> yawnDay;
    Map<String, Integer> yawnWeek;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_detail);
        toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        //My stuff ---------------------------------------------------------------------------------

        Intent intent = getIntent();
        if(intent != null){ currentUser = intent.getStringExtra("email"); }
        getSupportActionBar().setTitle(currentUser);

        //Get Widgets
        blinkFreq = findViewById(R.id.blinkFreq);

        EyeTitle = findViewById(R.id.EYETitle);
        EyeDay = findViewById(R.id.buttonEyeDay);
        EyeHour = findViewById(R.id.buttonEyeHour);
        EyeTime = findViewById(R.id.buttonEyeTime);
        EyeGraph = findViewById(R.id.graphEye);
        EyeTimestamps = findViewById(R.id.timestampsEye);

        YawnTitle = findViewById(R.id.YawnTitle);
        YawnDay = findViewById(R.id.buttonYawnDay);
        YawnHour = findViewById(R.id.buttonYawnHour);
        YawnTime = findViewById(R.id.buttonYawnTime);
        YawnGraph = findViewById(R.id.graphYawn);
        YawnTimestamps = findViewById(R.id.timestampsYawn);

        EyeDay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EyeHour.setChecked(false);
                EyeTime.setChecked(false);
                EyeGraph.setVisibility(View.VISIBLE);
                EyeTimestamps.setVisibility(View.GONE);
                populateGraph(EyeGraph, eyeDay, true);
            }
        });
        EyeHour.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EyeDay.setChecked(false);
                EyeTime.setChecked(false);
                EyeGraph.setVisibility(View.VISIBLE);
                EyeTimestamps.setVisibility(View.GONE);
                populateGraph(EyeGraph, eyeWeek, false);
            }
        });
        EyeTime.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EyeHour.setChecked(false);
                EyeDay.setChecked(false);
                EyeGraph.setVisibility(View.GONE);
                EyeTimestamps.setVisibility(View.VISIBLE);
            }
        });
        YawnDay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                YawnHour.setChecked(false);
                YawnTime.setChecked(false);
                YawnGraph.setVisibility(View.VISIBLE);
                YawnTimestamps.setVisibility(View.GONE);
                populateGraph(YawnGraph, yawnDay, true);
            }
        });
        YawnHour.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                YawnDay.setChecked(false);
                YawnTime.setChecked(false);
                YawnGraph.setVisibility(View.VISIBLE);
                YawnTimestamps.setVisibility(View.GONE);
                populateGraph(YawnGraph, yawnWeek, false);
            }
        });
        YawnTime.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                YawnHour.setChecked(false);
                YawnDay.setChecked(false);
                YawnGraph.setVisibility(View.GONE);
                YawnTimestamps.setVisibility(View.VISIBLE);
            }
        });

        referenceDatabase();
    }

    public void referenceDatabase(){
        getSupportActionBar().setTitle(currentUser);

        ref = database.getReference("users");

        NavigationView navView = findViewById(R.id.nav_view);
        final Menu menu = navView.getMenu();
        menu.clear();

        ref.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                menu.clear();
                for(final DataSnapshot snapshot: dataSnapshot.getChildren()){
                    menu.add(snapshot.getKey());
                    if(snapshot.getKey().matches(currentUser)){
                        userSnapshot = snapshot;
                        updateUI();
                    }
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        View header = navView.getHeaderView(0);
        if(mAuth.getCurrentUser() != null)
            ((TextView)header.findViewById(R.id.superUserEmail)).setText(mAuth.getCurrentUser().getEmail());
    }

    public void updateUI(){
        eyeDay = new HashMap<>();
        eyeWeek = new HashMap<>();
        yawnDay = new HashMap<>();
        yawnWeek = new HashMap<>();

        for(int i = 1; i < 8; i++){
            eyeDay.put(String.valueOf(i), 0);
            yawnDay.put(String.valueOf(i), 0);
        }
        for(int i = 0; i < 23; i++){
            eyeWeek.put(String.valueOf(i), 0);
            yawnWeek.put(String.valueOf(i), 0);
        }

        SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy - hh:mm:ss a", Locale.US);
        SimpleDateFormat sdfDAY = new SimpleDateFormat("u", Locale.US);
        SimpleDateFormat sdfWEEK = new SimpleDateFormat("HH", Locale.US);

        blinkFreq.setText(String.valueOf(userSnapshot.child("blink frequency").getValue(Integer.class)));

        EyeTimestamps.removeAllViews();
        YawnTimestamps.removeAllViews();

        int eyeStamp = userSnapshot.child("current eye timestamp").getValue(Integer.class);
        int yawnStamp = userSnapshot.child("current yawn timestamp").getValue(Integer.class);
        EyeTitle.setText("Drowsiness Detected (EYE): "+String.valueOf(eyeStamp));
        YawnTitle.setText("Drowsiness Detected (YAWN): "+String.valueOf(yawnStamp));

        DataSnapshot timestamps = userSnapshot.child("timestamp");
        for(int i = 0; i < eyeStamp; i++){
            try {
                TextView textView = new TextView(UserDetail.this);
                Long time = timestamps.child("Eye " + Integer.toString(i)).getValue(Long.class);
                Date date = new Date(time * 1000);
                textView.setText(sdf.format(date));
                EyeTimestamps.addView(textView);

                String day = sdfDAY.format(date);
                String week = sdfWEEK.format(date);
                eyeDay.put(day, eyeDay.get(day) + 1);
                eyeWeek.put(week, eyeWeek.get(week) + 1);
            }catch (Exception e){}
        }
        for(int i = 0; i < yawnStamp; i++){
            try {
                TextView textView = new TextView(UserDetail.this);
                Long time = timestamps.child("Yawn " + Integer.toString(i)).getValue(Long.class);
                Date date = new Date(time * 1000);
                textView.setText(sdf.format(date));
                YawnTimestamps.addView(textView);

                String day = sdfDAY.format(date);
                String week = sdfWEEK.format(date);
                yawnDay.put(day, yawnDay.get(day) + 1);
                yawnWeek.put(week, yawnWeek.get(week) + 1);
            }catch (Exception e){}
        }

        populateGraph(EyeGraph, eyeDay, true);
        populateGraph(YawnGraph, yawnDay, true);
    }

    public void populateGraph(GraphView graph, Map<String, Integer> map, boolean isDay){
        graph.removeAllSeries();
        graph.getGridLabelRenderer().setLabelFormatter(new StaticLabelsFormatter(graph));
        BarGraphSeries<DataPoint> series = new BarGraphSeries<>();
        graph.getViewport().setScalable(true);

        graph.getViewport().setMinX(0);
        graph.getViewport().setMaxX(23);

        int max = 23;
        String[] labels;
        if(isDay){
            graph.getViewport().setMinX(1);
            graph.getViewport().setMaxX(7);
            labels = new String[] {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};
            StaticLabelsFormatter staticLabelsFormatter = new StaticLabelsFormatter(graph);
            staticLabelsFormatter.setHorizontalLabels(labels);
            graph.getGridLabelRenderer().setLabelFormatter(staticLabelsFormatter);
            max = 7;
        }

        List<Map.Entry<String, Integer>> entryList = new ArrayList<Map.Entry<String, Integer>>(
                map.entrySet()
        );
        Collections.sort(
                entryList,
                new Comparator<Map.Entry<String, Integer>>() {
                    @Override
                    public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                        return Integer.compare(Integer.parseInt(o1.getKey()), Integer.parseInt(o2.getKey()));
                    }
                }
        );

        for(Map.Entry<String, Integer> e : entryList){
            int keyInt = Integer.parseInt(e.getKey());
            series.appendData(new DataPoint(keyInt, e.getValue()), true, max);
        }
        series.setDrawValuesOnTop(true);
        graph.getViewport().setScalable(false);
        graph.addSeries(series);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            if(doubleBackToExitPressedOnce){
                super.onBackPressed();
                finish();
            }

            this.doubleBackToExitPressedOnce = true;
            Toast.makeText(this, "Please click BACK again to exit", Toast.LENGTH_SHORT).show();

            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    doubleBackToExitPressedOnce=false;
                }
            }, 2000);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.user_detail, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            logout();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        currentUser = item.getTitle().toString();
        referenceDatabase();

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    /**
     * Logs out of the app or goes back to the login screen to log in
     */
    public void logout(){
        FirebaseAuth mAuth = FirebaseAuth.getInstance();
        mAuth.signOut();

        Intent intent = new Intent(UserDetail.this, MainActivity.class);
        intent.putExtra("skip", 1);
        startActivity(intent);
        finish();
    }
}

﻿import sys
import arcpy

import arcsdm;

from arcsdm import *
from arcsdm.sitereduction import ReduceSites
from arcsdm.calculateweights import Calculate
from arcsdm.categoricalmembership import Calculate
   

import importlib
from imp import reload;


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        
        self.label = "ArcSDM python toolbox"
        self.alias = "ArcSDM" 

        # List of tool classes associated with this toolbox
        self.tools = [CalculateWeightsTool,SiteReductionTool,CategoricalMembershipToool,CategoricalAndReclassTool]



class CalculateWeightsTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Weights"
        self.description = "Calculate weight rasters from the inputs"
        self.canRunInBackground = False
        self.category = "Weights of Evidence"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Evidence Raster Layer",
        name="evidence_raster_layer",
        datatype="GPRasterLayer",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Evidence raster codefield",
        name="Evidence_Raster_Code_Field",
        datatype="Field",
        parameterType="Optional",
        direction="Input")

        paramTrainingPoints = arcpy.Parameter(
        displayName="Training points",
        name="Training_points",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input")
        
        param2 = arcpy.Parameter(
        displayName="Type",
        name="Type",
        datatype="GPString",
        parameterType="Required",
        direction="Input")
        param2.filter.type = "ValueList";
        param2.filter.list = ["Descending", "Ascending", "Categorical", "Unique"];
        param2.value = "Descending";
        
        param3 = arcpy.Parameter(
        displayName="Output weights table",
        name="output_weights_table",
        datatype="DETable",
        parameterType="Required",
        direction="Output")

        param4 = arcpy.Parameter(
        displayName="Confidence Level of Studentized Contrast",
        name="Confidence_Level_of_Studentized_Contrast",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input")
        param4.value = "2";
                           
        param5 = arcpy.Parameter(
        displayName="Unit area (km2)",
        name="Unit_Area__sq_km_",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input")
        
        
        param6 = arcpy.Parameter(
        displayName="Missing data value",
        name="Missing_Data_Value",
        datatype="GPLong",
        parameterType="Required",
        direction="Input")
        param6.value = "-99";

                           
                                  
        params = [param0, param1, paramTrainingPoints, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
     
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #3.4
        try:
            importlib.reload (arcsdm.calculateweights)
        except :
            reload(arcsdm.calculateweights);
        # To list what functions does module contain
        #messages.addWarningMessage(dir(arcsdm.SiteReduction));
        #arcsdm.CalculateWeights.Calculate(self, parameters, messages);
        #messages.AddMessage("Waiting for debugger")
        #wait_for_debugger(15);
        calculateweights.Calculate(self, parameters, messages)
        return
        
        

        
        
        
class SiteReductionTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Training sites reduction"
        self.description = "Selects subset of the training points"
        self.canRunInBackground = False
        self.category = "Weights of Evidence"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Training sites layer",
        name="Training_Sites_layer",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Thinning selection",
        name="Thinning_Selection",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Unit area (sq km)",
        name="Unit_Area__sq_km_",
        datatype="GPLong",
        parameterType="Optional",
        direction="Input")
        
# Tämä vois olla hyvinkin valintalaatikko?
        param3 = arcpy.Parameter(
        displayName="Random selection",
        name="Random_selection",
        datatype="Boolean",
        parameterType="Optional",
        direction="Input")

        param4 = arcpy.Parameter(
        displayName="Random percentage selection",
        name="Random_percentage_selection",
        datatype="GPLong",
        parameterType="Optional",
        direction="Input")
                                            
        params = [param0, param1, param2, param3, param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].value == True:
            parameters[2].enabled = True;
        else:
            parameters[2].enabled = False;            
            
        if parameters[3].value == True:
            parameters[4].enabled = True;
        
        else:
            parameters[4].enabled = False;  
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        l = 0;
        
        if parameters[1].value == True:
            #parameters[4].setErrorMessage("Random percentage value required!")
            l = l + 1;
            if parameters[2].value == '' or  parameters[2].value is None:
                parameters[2].setErrorMessage("Thinning value required!")
                
        if parameters[3].value == True:
            l = l + 1;            
            #parameters[4].setErrorMessage("Random percentage value required!")
            if parameters[4].value == '' or  parameters[4].value is None:
                parameters[4].setErrorMessage("Random percentage value required!")
            elif parameters[4].value > 100 or parameters[4].value < 1:
                parameters[4].setErrorMessage("Value has to between 1-100 %!")
            
        if (l < 1):
            parameters[1].setErrorMessage("You have to select either one!")
            parameters[3].setErrorMessage("You have to select either one!")
        
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            importlib.reload (arcsdm.sitereduction)
        except :
            reload(sitereduction);
        sitereduction.ReduceSites(self, parameters, messages)
        return
        
class CategoricalMembershipToool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Categorical Membership"
        self.description = "Create fuzzy memberships for categorical data by first reclassification to integers and then division by an appropriate value"
        self.canRunInBackground = False
        self.category = "Fuzzy Logic\\Fuzzy Membership"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Categorical evidence raster",
        name="categorical_evidence",
        datatype="GPRasterLayer",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Reclassification",
        name="reclassification",
        datatype="GPTableView",
        parameterType="Required",
        direction="Input")

        param2 = arcpy.Parameter(
        displayName="Rescale Constant",
        name="rescale_constant",
        datatype="GPLong",
        parameterType="Required",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="FMCat",
        name="fmcat",
        datatype="DERasterDataset",
        parameterType="Required",
        direction="Output")
        
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            importlib.reload (arcsdm.categoricalmembership)
        except:
            reload(arcsdm.categoricalmembership)
        categoricalmembership.Calculate(self, parameters, messages)
        return

class CategoricalAndReclassTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Categorical & Reclass"
        self.description = "Create fuzzy memberships for categorical data by first reclassification to integers and then division by an appropriate value."
        self.canRunInBackground = False
        self.category = "Fuzzy Logic\\Fuzzy Membership"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Categorical evidence raster",
        name="categorical_evidence",
        datatype="GPRasterLayer",
        parameterType="Required",
        direction="Input")
        
        param1 = arcpy.Parameter(
        displayName="Reclass field",
        name="reclass_field",
        datatype="Field",
        parameterType="Required",
        direction="Input")
        
        param2 = arcpy.Parameter(
        displayName="Reclassification",
        name="reclassification",
        datatype="remap",
        parameterType="Required",
        direction="Input")
        
        param3 = arcpy.Parameter(
        displayName="FM Categorical",
        name="fmcat",
        datatype="DERasterDataset",
        parameterType="Required",
        direction="Output")

        param4 = arcpy.Parameter(
        displayName="Divisor",
        name="divisor",
        datatype="GPLong",
        parameterType="Required",
        direction="Input")
        
        param1.value = "VALUE"
        param1.enabled = False
        param2.enabled = False
        param1.parameterDependencies = [param0.name]  
        param2.parameterDependencies = [param0.name,param1.name]

        params = [param0,param1,param2,param3,param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
    
    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].value:
            parameters[1].enabled = True
            parameters[2].enabled = True
        else:
            parameters[1].enabled = False
            parameters[2].enabled = False
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            importlib.reload (arcsdm.categoricalreclass)
        except:
            reload(arcsdm.categoricalreclass)
        categoricalreclass.Calculate(self, parameters, messages)
        return
        
